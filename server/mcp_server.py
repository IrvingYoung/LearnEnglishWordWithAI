from mcp.server.fastmcp import FastMCP
import json
from datetime import datetime, timedelta
import os
import sqlite3
from typing import List, Dict, Optional, Any, Union

# Create an MCP server for English Word Learning
mcp = FastMCP("EnglishWordLearning")

# Initialize SQLite database
DB_PATH = os.path.join(os.path.dirname(__file__), 'english_words.db')

def init_db():
    """Initialize the database with the necessary tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create words table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT UNIQUE NOT NULL,
        pronunciation TEXT,
        translations TEXT,
        definitions TEXT,
        examples TEXT,
        notes TEXT,
        created_at TIMESTAMP,
        updated_at TIMESTAMP
    )
    ''')
    
    # Create study sessions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS study_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_id INTEGER NOT NULL,
        study_time INTEGER NOT NULL,
        recall_score INTEGER NOT NULL,
        studied_at TIMESTAMP NOT NULL,
        FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE
    )
    ''')
    
    # Create review schedule table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS review_schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word_id INTEGER NOT NULL,
        next_review TIMESTAMP NOT NULL,
        ease_factor REAL NOT NULL DEFAULT 2.5,
        interval INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (word_id) REFERENCES words(id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()

# Helper functions for database operations
def dict_to_json(data: Dict) -> str:
    """Convert dictionary to JSON string"""
    return json.dumps(data)

def json_to_dict(json_str: str) -> Dict:
    """Convert JSON string to dictionary"""
    return json.loads(json_str) if json_str else {}

def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO format"""
    return dt.isoformat()

def get_word_by_id(word_id: int) -> Dict:
    """Get a word by ID from the database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM words WHERE id = ?", (word_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
    
    word = dict(row)
    word['translations'] = json.loads(word['translations'])
    word['definitions'] = json.loads(word['definitions'])
    word['examples'] = json.loads(word['examples'])
    
    conn.close()
    return word

def get_word_by_text(word_text: str) -> Dict:
    """Get a word by text from the database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM words WHERE word = ?", (word_text,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return None
    
    word = dict(row)
    word['translations'] = json.loads(word['translations'])
    word['definitions'] = json.loads(word['definitions'])
    word['examples'] = json.loads(word['examples'])
    
    conn.close()
    return word

# Word Management API tools

@mcp.tool()
def saveWord(
    word: str, 
    pronunciation: str, 
    translations: List[str], 
    definitions: List[str], 
    examples: List[str], 
    notes: str
) -> Dict[str, Any]:
    """
    Store a new word and its information in the database
    
    Args:
        word: The English word to save
        pronunciation: Phonetic pronunciation
        translations: List of Chinese translations
        definitions: List of English definitions
        examples: Example sentences using the word
        notes: Additional usage notes
        
    Returns:
        Word ID and status
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if word already exists
        cursor.execute("SELECT id FROM words WHERE word = ?", (word,))
        existing = cursor.fetchone()
        
        if existing:
            word_id = existing[0]
            conn.close()
            return {
                "status": "error",
                "message": "Word already exists",
                "word_id": word_id
            }
        
        # Prepare data
        now = format_timestamp(datetime.utcnow())
        translations_json = dict_to_json(translations)
        definitions_json = dict_to_json(definitions)
        examples_json = dict_to_json(examples)
        
        # Insert word
        cursor.execute(
            """
            INSERT INTO words 
            (word, pronunciation, translations, definitions, examples, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, 
            (word, pronunciation, translations_json, definitions_json, examples_json, notes, now, now)
        )
        
        # Get the ID of the inserted word
        word_id = cursor.lastrowid
        
        conn.commit()
        conn.close()
        
        # Return the word info
        word_data = get_word_by_id(word_id)
        
        return {
            "status": "success",
            "message": "Word saved successfully",
            "word_id": word_id,
            "word": word_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def getWord(word_id: int = None, word: str = None) -> Dict[str, Any]:
    """
    Retrieve information about a specific word
    
    Args:
        word_id: Word identifier (numeric ID)
        word: The actual word text (alternative to word_id)
        
    Returns:
        Complete word information
    """
    try:
        if word_id is not None:
            word_data = get_word_by_id(word_id)
        elif word is not None:
            word_data = get_word_by_text(word)
        else:
            return {
                "status": "error",
                "message": "Either word_id or word must be provided"
            }
        
        if not word_data:
            return {
                "status": "error",
                "message": "Word not found"
            }
        
        return {
            "status": "success",
            "word": word_data
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def updateWord(word_id: int, fieldToUpdate: str, newValue: Union[str, List[str]]) -> Dict[str, Any]:
    """
    Update information for an existing word
    
    Args:
        word_id: Word identifier
        fieldToUpdate: Field to be updated
        newValue: New value for the field (string for word/pronunciation/notes, list for translations/definitions/examples)
        
    Returns:
        Updated word information
    """
    try:
        # Check if the field is valid
        valid_fields = ['word', 'pronunciation', 'translations', 'definitions', 'examples', 'notes']
        if fieldToUpdate not in valid_fields:
            return {
                "status": "error",
                "message": f"Invalid field: {fieldToUpdate}"
            }
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Check if word exists
        cursor.execute("SELECT * FROM words WHERE id = ?", (word_id,))
        word = cursor.fetchone()
        
        if not word:
            conn.close()
            return {
                "status": "error",
                "message": "Word not found"
            }
        
        # Prepare the new value
        if fieldToUpdate in ['translations', 'definitions', 'examples']:
            value = dict_to_json(newValue)
        else:
            value = newValue
            
        # Update the field
        now = format_timestamp(datetime.utcnow())
        cursor.execute(
            f"UPDATE words SET {fieldToUpdate} = ?, updated_at = ? WHERE id = ?",
            (value, now, word_id)
        )
        
        conn.commit()
        conn.close()
        
        # Get updated word
        updated_word = get_word_by_id(word_id)
        
        return {
            "status": "success",
            "message": "Word updated successfully",
            "word": updated_word
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def getAllWords() -> Dict[str, Any]:
    """
    Get a list of all words in the database
    
    Returns:
        Array of all words
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM words ORDER BY word")
        rows = cursor.fetchall()
        
        words = []
        for row in rows:
            word = dict(row)
            word['translations'] = json.loads(word['translations'])
            word['definitions'] = json.loads(word['definitions'])
            word['examples'] = json.loads(word['examples'])
            words.append(word)
        
        conn.close()
        
        return {
            "status": "success",
            "count": len(words),
            "words": words
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Learning Progress API tools

@mcp.tool()
def trackWordStudy(word_id: int, studyTime: int, recall: int) -> Dict[str, Any]:
    """
    Record a study session for a word and schedule next review
    
    Args:
        word_id: Word identifier
        studyTime: Time spent studying in seconds
        recall: Recall score (1-5, with 5 being perfect recall)
        
    Returns:
        Updated learning status with next review time
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if word exists
        cursor.execute("SELECT id FROM words WHERE id = ?", (word_id,))
        if not cursor.fetchone():
            conn.close()
            return {
                "status": "error",
                "message": f"Word with ID {word_id} not found"
            }
        
        # Record the study session
        now = datetime.utcnow()
        now_str = format_timestamp(now)
        
        cursor.execute(
            "INSERT INTO study_sessions (word_id, study_time, recall_score, studied_at) VALUES (?, ?, ?, ?)",
            (word_id, studyTime, recall, now_str)
        )
        
        # Get current schedule if exists
        cursor.execute("SELECT ease_factor, interval FROM review_schedule WHERE word_id = ?", (word_id,))
        schedule = cursor.fetchone()
        
        if schedule:
            ease_factor, interval = schedule
        else:
            ease_factor, interval = 2.5, 1  # Default values
        
        # Calculate new ease factor and interval based on SM-2 algorithm
        if recall < 3:
            # If recall was difficult, reset interval but adjust ease factor
            interval = 1
            ease_factor = max(1.3, ease_factor - 0.2)
        else:
            # Update ease factor
            ease_factor = ease_factor + (0.1 - (5 - recall) * (0.08 + (5 - recall) * 0.02))
            ease_factor = max(1.3, ease_factor)
            
            # Update interval
            if interval == 1:
                interval = 1
            elif interval == 2:
                interval = 6
            else:
                interval = round(interval * ease_factor)
        
        # Calculate next review date
        next_review = now + timedelta(days=interval)
        next_review_str = format_timestamp(next_review)
        
        # Update or insert review schedule
        if schedule:
            cursor.execute(
                "UPDATE review_schedule SET next_review = ?, ease_factor = ?, interval = ? WHERE word_id = ?",
                (next_review_str, ease_factor, interval, word_id)
            )
        else:
            cursor.execute(
                "INSERT INTO review_schedule (word_id, next_review, ease_factor, interval) VALUES (?, ?, ?, ?)",
                (word_id, next_review_str, ease_factor, interval)
            )
        
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "message": "Study session recorded",
            "word_id": word_id,
            "study_time": studyTime,
            "recall": recall,
            "next_review": next_review_str,
            "interval": interval,
            "ease_factor": ease_factor
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def getNextReviewWords(count: int = 10) -> Dict[str, Any]:
    """
    Get a list of words due for review based on spaced repetition
    
    Args:
        count: Number of words to return
        
    Returns:
        Array of words due for review
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        now = format_timestamp(datetime.utcnow())
        
        # Get words due for review
        cursor.execute("""
            SELECT w.* FROM words w
            JOIN review_schedule rs ON w.id = rs.word_id
            WHERE rs.next_review <= ?
            ORDER BY rs.next_review
            LIMIT ?
        """, (now, count))
        
        rows = cursor.fetchall()
        
        # If not enough words due for review, add words without schedules
        if len(rows) < count:
            remaining = count - len(rows)
            cursor.execute("""
                SELECT w.* FROM words w
                WHERE w.id NOT IN (SELECT word_id FROM review_schedule)
                ORDER BY w.created_at
                LIMIT ?
            """, (remaining,))
            rows.extend(cursor.fetchall())
        
        words = []
        for row in rows:
            word = dict(row)
            word['translations'] = json.loads(word['translations'])
            word['definitions'] = json.loads(word['definitions'])
            word['examples'] = json.loads(word['examples'])
            
            # Get review schedule info if available
            cursor.execute("SELECT next_review, interval FROM review_schedule WHERE word_id = ?", (word['id'],))
            schedule = cursor.fetchone()
            if schedule:
                word['next_review'] = schedule['next_review']
                word['interval'] = schedule['interval']
            
            words.append(word)
        
        conn.close()
        
        return {
            "status": "success",
            "count": len(words),
            "words": words
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@mcp.tool()
def getWordStats(word_id: int) -> Dict[str, Any]:
    """
    Retrieve learning statistics for a word
    
    Args:
        word_id: Word identifier
        
    Returns:
        Study history and performance metrics
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get word details
        cursor.execute("SELECT * FROM words WHERE id = ?", (word_id,))
        word_row = cursor.fetchone()
        
        if not word_row:
            conn.close()
            return {
                "status": "error",
                "message": f"Word with ID {word_id} not found"
            }
        
        word = dict(word_row)
        word['translations'] = json.loads(word['translations'])
        word['definitions'] = json.loads(word['definitions'])
        word['examples'] = json.loads(word['examples'])
        
        # Get study sessions
        cursor.execute("""
            SELECT study_time, recall_score, studied_at
            FROM study_sessions
            WHERE word_id = ?
            ORDER BY studied_at DESC
        """, (word_id,))
        
        sessions_rows = cursor.fetchall()
        sessions = [dict(row) for row in sessions_rows]
        
        # Get review schedule
        cursor.execute("""
            SELECT next_review, ease_factor, interval
            FROM review_schedule
            WHERE word_id = ?
        """, (word_id,))
        
        schedule_row = cursor.fetchone()
        schedule = dict(schedule_row) if schedule_row else None
        
        # Calculate metrics
        total_study_time = sum(session['study_time'] for session in sessions)
        avg_recall = sum(session['recall_score'] for session in sessions) / len(sessions) if sessions else 0
        study_count = len(sessions)
        
        conn.close()
        
        return {
            "status": "success",
            "word": word,
            "study_sessions": sessions,
            "schedule": schedule,
            "metrics": {
                "total_study_time": total_study_time,
                "avg_recall": avg_recall,
                "study_count": study_count,
                "first_studied": sessions[-1]['studied_at'] if sessions else None,
                "last_studied": sessions[0]['studied_at'] if sessions else None
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# Utility API tools

@mcp.tool()
def translateText(text: str, targetLanguage: str) -> Dict[str, Any]:
    """
    Translate text between English and Chinese
    
    Args:
        text: Text to translate
        targetLanguage: Target language code (en/zh)
        
    Returns:
        Translated text
    """
    # This is a placeholder implementation
    # In a real implementation, you would use a translation API
    if targetLanguage not in ['en', 'zh']:
        return {
            "status": "error",
            "message": "Invalid target language. Must be 'en' or 'zh'."
        }
    
    return {
        "status": "success",
        "original": text,
        "translated": f"[Translated {text} to {targetLanguage}]",
        "target_language": targetLanguage
    }

@mcp.tool()
def generateExamples(word: str, count: int = 3) -> Dict[str, Any]:
    """
    Generate additional example sentences for a word
    
    Args:
        word: The word to generate examples for
        count: Number of examples to generate
        
    Returns:
        Array of example sentences
    """
    # This is a placeholder implementation
    # In a real implementation, you would use an LLM to generate examples
    examples = [
        f"This is the first example using the word '{word}'.",
        f"Here's a second example with '{word}' in context.",
        f"The third example demonstrates how to use '{word}' in a different situation."
    ]
    
    return {
        "status": "success",
        "word": word,
        "examples": examples[:count]
    }

# Dynamic word resource for querying specific words
@mcp.resource("word://{word_id}")
def get_word_resource(word_id: str) -> Dict[str, Any]:
    """Get information about a specific word by ID"""
    try:
        word_id_int = int(word_id)
        return getWord(word_id=word_id_int)
    except ValueError:
        # If word_id is not an integer, treat it as the word text
        return getWord(word=word_id)

@mcp.tool()
def removeWordByText(word: str) -> Dict[str, Any]:
    """
    Remove a word from the database using the word text
    
    Args:
        word: The text of the word to be deleted
        
    Returns:
        Status of the deletion operation
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if word exists
        cursor.execute("SELECT id FROM words WHERE word = ?", (word,))
        word_row = cursor.fetchone()
        
        if not word_row:
            conn.close()
            return {
                "status": "error",
                "message": f"Word '{word}' not found"
            }
        
        word_id = word_row[0]
        
        # Delete the word
        cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
        
        # Commit changes
        conn.commit()
        
        conn.close()
        
        return {
            "status": "success",
            "message": f"Word '{word}' has been deleted successfully"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

# @mcp.tool()
# def removeSafeWord(word_id: int, word: str) -> Dict[str, Any]:
#     """
#     Safely remove a word from the database by checking both ID and text match
    
#     Args:
#         word_id: Word identifier to be deleted
#         word: Text of the word to be deleted (for verification)
        
#     Returns:
#         Status of the deletion operation
#     """
#     try:
#         conn = sqlite3.connect(DB_PATH)
#         conn.row_factory = sqlite3.Row
#         cursor = conn.cursor()
        
#         # Check if word exists with the given ID
#         cursor.execute("SELECT * FROM words WHERE id = ?", (word_id,))
#         word_row = cursor.fetchone()
        
#         if not word_row:
#             conn.close()
#             return {
#                 "status": "error",
#                 "message": f"Word with ID {word_id} not found"
#             }
        
#         # Convert to dictionary for easier access
#         word_data = dict(word_row)
        
#         # Verify the text matches the provided word parameter
#         if word_data['word'] != word:
#             conn.close()
#             return {
#                 "status": "error",
#                 "message": f"Word ID {word_id} corresponds to '{word_data['word']}', not '{word}'. Verification failed."
#             }
        
#         # Delete the word once verification is successful
#         cursor.execute("DELETE FROM words WHERE id = ?", (word_id,))
        
#         # Commit changes
#         conn.commit()
        
#         # Check if word was deleted
#         cursor.execute("SELECT * FROM words WHERE id = ?", (word_id,))
#         if cursor.fetchone():
#             conn.close()
#             return {
#                 "status": "error",
#                 "message": "Failed to delete word"
#             }
        
#         conn.close()
        
#         return {
#             "status": "success",
#             "message": f"Word '{word}' (ID: {word_id}) has been deleted successfully"
#         }
#     except Exception as e:
#         return {
#             "status": "error",
#             "message": str(e)
#         }

if __name__ == "__main__":
    # Start the MCP server
    mcp.run(transport="stdio") 