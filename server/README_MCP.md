# English Word Learning MCP Server

This is an implementation of the MCP (Model Control Protocol) server for the English Word Learning application using the `mcp.server.fastmcp` package.

## Overview

The FastMCP framework provides a simple way to create MCP-compliant servers with tools and resources. This implementation includes all the functionality specified in the API requirements but uses the FastMCP framework for easier integration with LLMs that support MCP.

## Setup

1. Install the FastMCP package:
```bash
pip install fastmcp
```

2. Install other dependencies:
```bash
pip install -r requirements_mcp.txt
```

3. Run the MCP server:

For stdio transport (default):
```bash
python mcp_server.py
```

For SSE transport:
```bash
python mcp_server.py --transport sse --host localhost --port 5000
```

Transport options:
- `stdio`: Standard input/output transport (default)
- `sse`: Server-Sent Events transport over HTTP
  - `--host`: Host to bind to (default: localhost)
  - `--port`: Port to bind to (default: 5000)

When using SSE transport, the server will be available at `http://<host>:<port>`.

## MCP Tools and Resources

The server provides the following MCP tools and resources:

### Word Management Tools

1. **saveWord**
   - **Description**: Store a new word and its information in the database
   - **Parameters**:
     - `word` (string): The English word to save
     - `pronunciation` (string): Phonetic pronunciation
     - `translations` (array): List of Chinese translations
     - `definitions` (array): List of English definitions
     - `examples` (array): Example sentences using the word
     - `notes` (string): Additional usage notes
   - **Returns**: Word ID and status

2. **getWord**
   - **Description**: Retrieve information about a specific word
   - **Parameters**:
     - `word_id` (integer, optional): Word identifier
     - `word` (string, optional): The actual word text
   - **Note**: Either `word_id` or `word` must be provided
   - **Returns**: Complete word information

3. **updateWord**
   - **Description**: Update information for an existing word
   - **Parameters**:
     - `word_id` (integer): Word identifier
     - `fieldToUpdate` (string): Field to be updated
     - `newValue` (any): New value for the field
   - **Returns**: Updated word information

4. **getAllWords**
   - **Description**: Get a list of all words
   - **Parameters**: None
   - **Returns**: Array of all words

5. **removeWordByText**
   - **Description**: Remove a word from the database using the word text
   - **Parameters**:
     - `word` (string): The text of the word to be deleted
   - **Returns**: Status of the deletion operation

6. **removeSafeWord**
   - **Description**: Safely remove a word by verifying both ID and text match
   - **Parameters**:
     - `word_id` (integer): Word identifier to be deleted
     - `word` (string): The text of the word to be deleted (for verification)
   - **Note**: Deletion only occurs if the word_id corresponds to the exact word text
   - **Returns**: Status of the deletion operation

### Learning Progress Tools

1. **trackWordStudy**
   - **Description**: Record a study session for a word
   - **Parameters**:
     - `word_id` (integer): Word identifier
     - `studyTime` (integer): Time spent studying in seconds
     - `recall` (integer): Recall score (1-5, with 5 being perfect recall)
   - **Returns**: Updated learning status

2. **getNextReviewWords**
   - **Description**: Get a list of words due for review based on spaced repetition
   - **Parameters**:
     - `count` (integer, optional): Number of words to return (default: 10)
   - **Returns**: Array of words due for review

### Utility Tools

1. **translateText**
   - **Description**: Translate text between English and Chinese
   - **Parameters**:
     - `text` (string): Text to translate
     - `targetLanguage` (string): Target language code (en/zh)
   - **Returns**: Translated text

2. **generateExamples**
   - **Description**: Generate additional example sentences for a word
   - **Parameters**:
     - `word` (string): The word to generate examples for
     - `count` (integer, optional): Number of examples to generate (default: 3)
   - **Returns**: Array of example sentences

### Resources

1. **word://{word_id}**
   - **Description**: Get information about a specific word
   - **Parameters**:
     - `word_id` (string): Either the word ID (integer) or the actual word text
   - **Returns**: Word information (same as getWord tool)

## Using MCP with an LLM

To use this MCP server with an LLM, configure the LLM to use the MCP protocol and point it to the server URL. The LLM will then be able to use the tools and resources provided by the server.

### Example Tool Call

```json
{
  "tool": "saveWord",
  "params": {
    "word": "example",
    "pronunciation": "ɪɡˈzæmpəl",
    "translations": ["例子", "实例", "榜样"],
    "definitions": ["something that serves as a pattern of behavior to be imitated", "a representative form or pattern"],
    "examples": ["This is an example of how the word is used.", "She set a good example for others to follow."],
    "notes": "Often used in phrases like 'for example' or 'lead by example'"
  }
}
```

### Example Remove Word By Text Call

```json
{
  "tool": "removeWordByText",
  "params": {
    "word": "example"
  }
}
```

### Example Safe Remove Word Call

```json
{
  "tool": "removeSafeWord",
  "params": {
    "word_id": 1,
    "word": "example"
  }
}
```

### Example Resource Request

```
GET /resources/word://1
```

or

```
GET /resources/word://example
```

## Testing

You can test the MCP server using the provided `test_mcp.py` script:

```bash
python test_mcp.py
```

This script demonstrates how to make calls to the MCP tools and resources. 