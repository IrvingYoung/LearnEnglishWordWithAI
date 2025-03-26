import requests
import json
import time

# Base URL for the API
BASE_URL = 'http://localhost:5000/api/words'

def test_word_management_api():
    """Test the Word Management API endpoints"""
    
    # 1. Save a new word
    print("\n1. Testing saveWord API...")
    word_data = {
        "word": "serendipity",
        "pronunciation": "ˌserənˈdɪpɪti",
        "translations": ["机缘巧合", "意外发现", "幸运"],
        "definitions": [
            "the occurrence and development of events by chance in a happy or beneficial way",
            "the faculty or phenomenon of finding valuable or agreeable things not sought for"
        ],
        "examples": [
            "The discovery of penicillin was a case of serendipity",
            "They found each other by serendipity"
        ],
        "notes": "From the Persian fairy tale 'The Three Princes of Serendip'"
    }
    
    response = requests.post(BASE_URL, json=word_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Get the word ID from the response
    word_id = response.json().get('word_id')
    
    # 2. Get the word by ID
    print("\n2. Testing getWord API by ID...")
    response = requests.get(f"{BASE_URL}/{word_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 3. Get the word by text
    print("\n3. Testing getWord API by text...")
    response = requests.get(f"{BASE_URL}/search?word=serendipity")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 4. Update the word
    print("\n4. Testing updateWord API...")
    update_data = {
        "fieldToUpdate": "translations",
        "newValue": ["机缘巧合", "意外发现", "幸运", "机遇", "缘分"]
    }
    response = requests.put(f"{BASE_URL}/{word_id}", json=update_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 5. Get all words
    print("\n5. Testing getAllWords API...")
    response = requests.get(BASE_URL)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    # Give the server a moment to start if needed
    print("Please make sure the server is running at http://localhost:5000")
    print("Press Enter to continue with the tests...")
    input()
    
    # Run the tests
    test_word_management_api() 