import requests
import json
import sys

# Explicitly use HTTP protocol
BASE_URL = 'http://localhost:5000'

def handle_request_error(func):
    """Decorator to handle request errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.SSLError as e:
            print(f"SSL Error: Make sure you're using http:// not https:// in the URL\nError: {e}", file=sys.stderr)
            return {"status": "error", "message": "SSL connection error"}
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: Make sure the server is running and accessible\nError: {e}", file=sys.stderr)
            return {"status": "error", "message": "Connection error"}
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return {"status": "error", "message": str(e)}
    return wrapper

@handle_request_error
def save_word(word: str, pronunciation: str, translations: list, 
              definitions: list, examples: list, notes: str):
    """Save a new word to the database"""
    url = f"{BASE_URL}/tools/saveWord"
    data = {
        "word": word,
        "pronunciation": pronunciation,
        "translations": translations,
        "definitions": definitions,
        "examples": examples,
        "notes": notes
    }
    response = requests.post(url, json=data)
    return response.json()

@handle_request_error
def get_word(word_id: int = None, word: str = None):
    """Get word information"""
    url = f"{BASE_URL}/tools/getWord"
    params = {}
    if word_id is not None:
        params['word_id'] = word_id
    if word is not None:
        params['word'] = word
    response = requests.get(url, params=params)
    return response.json()

@handle_request_error
def get_all_words():
    """Get all words from the database"""
    url = f"{BASE_URL}/tools/getAllWords"
    response = requests.get(url)
    return response.json()

@handle_request_error
def track_word_study(word_id: int, study_time: int, recall: int):
    """Record a study session for a word"""
    url = f"{BASE_URL}/tools/trackWordStudy"
    data = {
        "word_id": word_id,
        "studyTime": study_time,
        "recall": recall
    }
    response = requests.post(url, json=data)
    return response.json()

@handle_request_error
def get_next_review_words(count: int = 10):
    """Get words due for review"""
    url = f"{BASE_URL}/tools/getNextReviewWords"
    params = {"count": count}
    response = requests.get(url, params=params)
    return response.json()

if __name__ == "__main__":
    print(f"Connecting to MCP server at {BASE_URL}")
    print("Make sure the server is running with: python mcp_server.py --transport sse")
    print("Press Enter to continue...")
    input()

    # Example usage
    print("\nSaving a new word...")
    result = save_word(
        word="example",
        pronunciation="ɪɡˈzæmpəl",
        translations=["例子", "实例"],
        definitions=["a representative form or pattern"],
        examples=["This is an example sentence."],
        notes="Common word"
    )
    print(json.dumps(result, indent=2))

    if result["status"] == "error":
        print("\nError occurred. Make sure:")
        print("1. The server is running with: python mcp_server.py --transport sse")
        print("2. The server URL is correct (using http:// not https://)")
        print("3. The port number matches the server's port")
        sys.exit(1)

    print("\nGetting all words...")
    result = get_all_words()
    print(json.dumps(result, indent=2))

    print("\nGetting word by text...")
    result = get_word(word="example")
    print(json.dumps(result, indent=2))

    if result["status"] == "success" and "word" in result:
        word_id = result["word"]["id"]
        
        print("\nTracking study session...")
        result = track_word_study(
            word_id=word_id,
            study_time=300,  # 5 minutes
            recall=4         # Good recall
        )
        print(json.dumps(result, indent=2))

    print("\nGetting words for review...")
    result = get_next_review_words(count=5)
    print(json.dumps(result, indent=2)) 