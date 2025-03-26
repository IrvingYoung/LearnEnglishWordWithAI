from app import ma
from app.word_management.models import Word
from marshmallow import fields, post_load, pre_dump
import json

class WordSchema(ma.SQLAlchemyAutoSchema):
    """Schema for Word model serialization/deserialization."""
    
    class Meta:
        model = Word
        load_instance = True
        include_fk = True
    
    # Override JSON fields to handle serialization/deserialization
    translations = fields.List(fields.String(), required=False)
    definitions = fields.List(fields.String(), required=False)
    examples = fields.List(fields.String(), required=False)
    
    # Add URL for the resource
    url = ma.URLFor('word_management.get_word', values=dict(word_id='<id>'))
    
    @pre_dump
    def _pre_dump(self, word, **kwargs):
        """Convert JSON strings to Python lists before serialization."""
        word_dict = {
            'id': word.id,
            'word': word.word,
            'pronunciation': word.pronunciation,
            'translations': word.get_translations(),
            'definitions': word.get_definitions(),
            'examples': word.get_examples(),
            'notes': word.notes,
            'created_at': word.created_at,
            'updated_at': word.updated_at
        }
        return word_dict

word_schema = WordSchema()
words_schema = WordSchema(many=True) 