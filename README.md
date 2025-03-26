# Learn English Words With AI

A powerful application that helps you memorize and learn English vocabulary with the assistance of Large Language Models (LLMs) and Model Control Protocol (MCP).

## Overview

This application is designed to enhance your English vocabulary learning experience by leveraging AI to provide comprehensive word information. As you encounter new English words in your daily life, the application stores them along with detailed information to help you better understand and remember them.

## Key Features

- **Word Collection**: Easily add new English words you encounter in your daily life
- **AI-Powered Explanations**: Get detailed explanations of words from advanced LLMs
- **Bilingual Support**: Receive comprehensive Chinese translations and English definitions
- **Contextual Examples**: Learn how words are used in different contexts through example sentences
- **Spaced Repetition**: Review words at optimal intervals to maximize retention
- **Progress Tracking**: Monitor your vocabulary growth and learning progress
- **MCP Integration**: Utilize Model Control Protocol for efficient AI tool integration

## Technical Architecture

1. **Frontend**: User-friendly interface for inputting words and displaying information
2. **LLM Integration**: Connection to language models for generating word explanations
3. **MCP Server**: Implementation of tools API for LLM invocation
4. **Database**: Storage of word information including:
   - Original word and pronunciation
   - Detailed Chinese translations
   - Comprehensive English definitions
   - Multiple example sentences
   - Usage notes and common collocations
   - User learning progress

## MCP Server Interface

The MCP (Model Control Protocol) server provides a standardized interface for the LLM to interact with the application's database and functionality. Below are the key API endpoints:

### Word Management API

1. **saveWord**
   - **Description**: Store a new word and its information in the database
   - **Parameters**:
     - `word` (string): The English word to save
     - `pronunciation` (string): Phonetic pronunciation
     - `translations` (array): List of Chinese translations
     - `definitions` (array): List of English definitions
     - `examples` (array): Example sentences using the word
     - `notes` (string, optional): Additional usage notes
   - **Returns**: Word ID and status

2. **getWord**
   - **Description**: Retrieve information about a specific word
   - **Parameters**: 
     - `wordId` (string) or `word` (string): Identifier for the word
   - **Returns**: Complete word information

3. **updateWord**
   - **Description**: Update information for an existing word
   - **Parameters**:
     - `wordId` (string): Word identifier
     - `fieldToUpdate` (string): Field to be updated
     - `newValue` (any): New value for the field
   - **Returns**: Updated word information

### Learning Progress API

1. **trackWordStudy**
   - **Description**: Record a study session for a word
   - **Parameters**:
     - `wordId` (string): Word identifier
     - `studyTime` (number): Time spent studying in seconds
     - `recall` (number): Recall score (1-5, with 5 being perfect recall)
   - **Returns**: Updated learning status

2. **getNextReviewWords**
   - **Description**: Get a list of words due for review based on spaced repetition
   - **Parameters**:
     - `count` (number, optional): Number of words to return (default: 10)
   - **Returns**: Array of words due for review

3. **getWordStats**
   - **Description**: Retrieve learning statistics for a word
   - **Parameters**:
     - `wordId` (string): Word identifier
   - **Returns**: Study history and performance metrics

### Utility API

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
     - `count` (number, optional): Number of examples to generate (default: 3)
   - **Returns**: Array of example sentences

All API endpoints return responses in JSON format with appropriate status codes and error messages when applicable.

## Usage Flow

1. User encounters an unfamiliar English word
2. User inputs the word into the application
3. LLM processes the word using MCP tools
4. Word information is stored in the database
5. User reviews the word details and examples
6. Application schedules future review sessions based on learning progress

## Getting Started

[Installation and setup instructions will be added here]

## Contributing

[Contribution guidelines will be added here]

## License

[License information will be added here] 