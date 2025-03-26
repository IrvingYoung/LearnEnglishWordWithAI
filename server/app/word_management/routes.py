from flask import Blueprint, request, jsonify
from app import db
from app.word_management.models import Word
from app.word_management.schemas import word_schema, words_schema
import json

# Blueprint for word management routes
word_bp = Blueprint('word_management', __name__)

@word_bp.route('/', methods=['POST'])
def save_word():
    """
    API endpoint for saving a new word
    ---
    Implements the saveWord functionality as defined in the MCP interface
    """
    try:
        # Get data from request
        data = request.json
        
        # Check if word already exists
        existing_word = Word.query.filter_by(word=data.get('word')).first()
        if existing_word:
            return jsonify({
                'status': 'error',
                'message': 'Word already exists',
                'word_id': existing_word.id
            }), 409
        
        # Create new word instance
        word = Word(
            word=data.get('word'),
            pronunciation=data.get('pronunciation'),
            translations=data.get('translations'),
            definitions=data.get('definitions'),
            examples=data.get('examples'),
            notes=data.get('notes')
        )
        
        # Save to database
        db.session.add(word)
        db.session.commit()
        
        # Return response
        return jsonify({
            'status': 'success',
            'message': 'Word saved successfully',
            'word_id': word.id,
            'word': word_schema.dump(word)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@word_bp.route('/<int:word_id>', methods=['GET'])
def get_word(word_id):
    """
    API endpoint for retrieving a word by ID
    ---
    Implements the getWord functionality as defined in the MCP interface
    """
    try:
        # Find word by ID
        word = Word.query.get(word_id)
        
        if not word:
            return jsonify({
                'status': 'error',
                'message': 'Word not found'
            }), 404
        
        # Return word information
        return jsonify({
            'status': 'success',
            'word': word_schema.dump(word)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@word_bp.route('/search', methods=['GET'])
def search_word_by_text():
    """
    API endpoint for retrieving a word by its text
    ---
    Alternative implementation of getWord that searches by word text
    """
    try:
        # Get word text from query parameter
        word_text = request.args.get('word')
        
        if not word_text:
            return jsonify({
                'status': 'error',
                'message': 'Word parameter is required'
            }), 400
        
        # Find word by text
        word = Word.query.filter_by(word=word_text).first()
        
        if not word:
            return jsonify({
                'status': 'error',
                'message': 'Word not found'
            }), 404
        
        # Return word information
        return jsonify({
            'status': 'success',
            'word': word_schema.dump(word)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@word_bp.route('/<int:word_id>', methods=['PUT'])
def update_word(word_id):
    """
    API endpoint for updating a word
    ---
    Implements the updateWord functionality as defined in the MCP interface
    """
    try:
        # Get data from request
        data = request.json
        
        # Find word by ID
        word = Word.query.get(word_id)
        
        if not word:
            return jsonify({
                'status': 'error',
                'message': 'Word not found'
            }), 404
        
        # Get field to update and new value
        field_to_update = data.get('fieldToUpdate')
        new_value = data.get('newValue')
        
        if not field_to_update or new_value is None:
            return jsonify({
                'status': 'error',
                'message': 'fieldToUpdate and newValue are required'
            }), 400
        
        # Check if field exists in the model
        if field_to_update not in ['word', 'pronunciation', 'translations', 
                                 'definitions', 'examples', 'notes']:
            return jsonify({
                'status': 'error',
                'message': f'Invalid field: {field_to_update}'
            }), 400
        
        # Update field
        word.update_field(field_to_update, new_value)
        
        # Save changes
        db.session.commit()
        
        # Return updated word
        return jsonify({
            'status': 'success',
            'message': 'Word updated successfully',
            'word': word_schema.dump(word)
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@word_bp.route('/', methods=['GET'])
def get_all_words():
    """API endpoint for retrieving all words"""
    try:
        words = Word.query.all()
        return jsonify({
            'status': 'success',
            'count': len(words),
            'words': words_schema.dump(words)
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500 