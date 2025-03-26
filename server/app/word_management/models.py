from app import db
from datetime import datetime
import json

class Word(db.Model):
    """Model for English words and their related information."""
    
    __tablename__ = 'words'
    
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, unique=True)
    pronunciation = db.Column(db.String(200))
    translations = db.Column(db.Text)  # Stored as JSON string
    definitions = db.Column(db.Text)   # Stored as JSON string
    examples = db.Column(db.Text)      # Stored as JSON string
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, word, pronunciation=None, translations=None, definitions=None, 
                 examples=None, notes=None):
        self.word = word
        self.pronunciation = pronunciation
        self.translations = json.dumps(translations or [])
        self.definitions = json.dumps(definitions or [])
        self.examples = json.dumps(examples or [])
        self.notes = notes
    
    def get_translations(self):
        """Return translations as a Python list."""
        return json.loads(self.translations)
    
    def get_definitions(self):
        """Return definitions as a Python list."""
        return json.loads(self.definitions)
    
    def get_examples(self):
        """Return examples as a Python list."""
        return json.loads(self.examples)
    
    def update_field(self, field, value):
        """Update a specific field with a new value."""
        if field in ['translations', 'definitions', 'examples']:
            setattr(self, field, json.dumps(value))
        else:
            setattr(self, field, value)
        self.updated_at = datetime.utcnow()
        
    def __repr__(self):
        return f'<Word {self.word}>' 