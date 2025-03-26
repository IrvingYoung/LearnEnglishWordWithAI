# MCP Server for English Word Learning

This directory contains the implementation of the MCP (Model Control Protocol) server for the English Word Learning application. The server provides APIs for managing English words and their related information.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python run.py
```

By default, the server runs on http://localhost:5000

## API Documentation

### Word Management API

#### 1. Save Word (POST `/api/words/`)

Stores a new word and its information in the database.

**Request Body:**
```json
{
  "word": "example",
  "pronunciation": "ɪɡˈzæmpəl",
  "translations": ["例子", "实例", "榜样"],
  "definitions": ["something that serves as a pattern of behavior to be imitated", "a representative form or pattern"],
  "examples": ["This is an example of how the word is used.", "She set a good example for others to follow."],
  "notes": "Often used in phrases like 'for example' or 'lead by example'"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Word saved successfully",
  "word_id": 1,
  "word": {
    "id": 1,
    "word": "example",
    "pronunciation": "ɪɡˈzæmpəl",
    "translations": ["例子", "实例", "榜样"],
    "definitions": ["something that serves as a pattern of behavior to be imitated", "a representative form or pattern"],
    "examples": ["This is an example of how the word is used.", "She set a good example for others to follow."],
    "notes": "Often used in phrases like 'for example' or 'lead by example'",
    "created_at": "2024-03-26T15:30:45.123456",
    "updated_at": "2024-03-26T15:30:45.123456",
    "url": "/api/words/1"
  }
}
```

#### 2. Get Word (GET `/api/words/{word_id}`)

Retrieves information about a specific word by its ID.

**Response:**
```json
{
  "status": "success",
  "word": {
    "id": 1,
    "word": "example",
    "pronunciation": "ɪɡˈzæmpəl",
    "translations": ["例子", "实例", "榜样"],
    "definitions": ["something that serves as a pattern of behavior to be imitated", "a representative form or pattern"],
    "examples": ["This is an example of how the word is used.", "She set a good example for others to follow."],
    "notes": "Often used in phrases like 'for example' or 'lead by example'",
    "created_at": "2024-03-26T15:30:45.123456",
    "updated_at": "2024-03-26T15:30:45.123456",
    "url": "/api/words/1"
  }
}
```

#### 3. Search Word by Text (GET `/api/words/search?word={word_text}`)

Retrieves information about a specific word by its text.

**Response:** Same as Get Word

#### 4. Update Word (PUT `/api/words/{word_id}`)

Updates information for an existing word.

**Request Body:**
```json
{
  "fieldToUpdate": "translations",
  "newValue": ["例子", "实例", "榜样", "范例"]
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Word updated successfully",
  "word": {
    "id": 1,
    "word": "example",
    "pronunciation": "ɪɡˈzæmpəl",
    "translations": ["例子", "实例", "榜样", "范例"],
    "definitions": ["something that serves as a pattern of behavior to be imitated", "a representative form or pattern"],
    "examples": ["This is an example of how the word is used.", "She set a good example for others to follow."],
    "notes": "Often used in phrases like 'for example' or 'lead by example'",
    "created_at": "2024-03-26T15:30:45.123456",
    "updated_at": "2024-03-26T15:32:10.987654",
    "url": "/api/words/1"
  }
}
```

#### 5. Get All Words (GET `/api/words/`)

Retrieves a list of all words in the database.

**Response:**
```json
{
  "status": "success",
  "count": 1,
  "words": [
    {
      "id": 1,
      "word": "example",
      "pronunciation": "ɪɡˈzæmpəl",
      "translations": ["例子", "实例", "榜样", "范例"],
      "definitions": ["something that serves as a pattern of behavior to be imitated", "a representative form or pattern"],
      "examples": ["This is an example of how the word is used.", "She set a good example for others to follow."],
      "notes": "Often used in phrases like 'for example' or 'lead by example'",
      "created_at": "2024-03-26T15:30:45.123456",
      "updated_at": "2024-03-26T15:32:10.987654",
      "url": "/api/words/1"
    }
  ]
}
```

## Error Handling

All API endpoints return appropriate HTTP status codes and error messages in case of failure.

Example error response:
```json
{
  "status": "error",
  "message": "Word not found"
}
```

Common status codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 404: Not Found
- 409: Conflict (e.g., word already exists)
- 500: Internal Server Error 