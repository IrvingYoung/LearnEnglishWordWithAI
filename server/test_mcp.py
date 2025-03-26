import requests
import json
import time

# Base URL for the MCP server
BASE_URL = 'http://localhost:5000'

def test_word_management_api():
    """Test the Word Management API tools via MCP"""
    
    # 1. Save a new word using saveWord tool
    print("\n1. Testing saveWord tool...")
    request_data = {
        "tool": "saveWord",
        "params": {
            "word": "eloquent",
            "pronunciation": "ˈɛləkwənt",
            "translations": ["雄辩的", "流利的", "有说服力的"],
            "definitions": [
                "fluent or persuasive in speaking or writing",
                "clearly expressing or indicating something"
            ],
            "examples": [
                "She gave an eloquent speech about human rights",
                "His silence was more eloquent than words"
            ],
            "notes": "From Latin eloquens, from eloqui 'speak out'"
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    # Get the word ID from the response
    word_id = result.get('result', {}).get('word_id')
    
    # 2. Get the word by ID using getWord tool
    print("\n2. Testing getWord tool with ID...")
    request_data = {
        "tool": "getWord",
        "params": {
            "word_id": word_id
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 3. Get the word by text using getWord tool
    print("\n3. Testing getWord tool with text...")
    request_data = {
        "tool": "getWord",
        "params": {
            "word": "eloquent"
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 4. Update the word using updateWord tool
    print("\n4. Testing updateWord tool...")
    request_data = {
        "tool": "updateWord",
        "params": {
            "word_id": word_id,
            "fieldToUpdate": "translations",
            "newValue": ["雄辩的", "流利的", "有说服力的", "善于表达的"]
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 5. Get all words using getAllWords tool
    print("\n5. Testing getAllWords tool...")
    request_data = {
        "tool": "getAllWords",
        "params": {}
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 6. Test the dynamic resource for word lookup
    print("\n6. Testing word resource...")
    response = requests.get(f"{BASE_URL}/resources/word://{word_id}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # Add additional test words for deletion tests
    print("\n7. Adding test words for deletion...")
    
    # Add word for verification deletion
    verification_word_data = {
        "tool": "saveWord",
        "params": {
            "word": "meticulous",
            "pronunciation": "məˈtɪkjʊləs",
            "translations": ["一丝不苟的", "细致的", "精确的"],
            "definitions": [
                "showing great attention to detail",
                "very careful and precise"
            ],
            "examples": [
                "She is meticulous about her work",
                "He took meticulous notes during the lecture"
            ],
            "notes": "From Latin meticulosus, fearful, timid"
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=verification_word_data)
    verification_result = response.json()
    verification_word_id = verification_result.get('result', {}).get('word_id')
    
    # Add word for text-based deletion
    request_data = {
        "tool": "saveWord",
        "params": {
            "word": "ephemeral",
            "pronunciation": "ɪˈfɛm(ə)rəl",
            "translations": ["短暂的", "瞬息的"],
            "definitions": [
                "lasting for a very short time",
                "transitory"
            ],
            "examples": [
                "The ephemeral nature of fashion trends",
                "His fame was ephemeral"
            ],
            "notes": "From Greek ephēmeros, lasting only a day"
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    ephemeral_result = response.json()
    print(f"Saved additional test words")
    
    # 8. Test removeSafeWord tool with correct verification
    print("\n8. Testing removeSafeWord tool (correct verification)...")
    request_data = {
        "tool": "removeSafeWord",
        "params": {
            "word_id": verification_word_id,
            "word": "meticulous"
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 9. Test removeSafeWord tool with incorrect verification
    print("\n9. Testing removeSafeWord tool (incorrect verification)...")
    request_data = {
        "tool": "removeSafeWord",
        "params": {
            "word_id": word_id,
            "word": "wrong_word"  # This should fail verification
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 10. Test removeWordByText tool
    print("\n10. Testing removeWordByText tool...")
    request_data = {
        "tool": "removeWordByText",
        "params": {
            "word": "eloquent"
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 11. Test removeWordByText tool with ephemeral word
    print("\n11. Testing removeWordByText with another word...")
    request_data = {
        "tool": "removeWordByText",
        "params": {
            "word": "ephemeral"
        }
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    # 12. Verify that words were deleted by getting all words
    print("\n12. Verifying deletion with getAllWords...")
    request_data = {
        "tool": "getAllWords",
        "params": {}
    }
    
    response = requests.post(f"{BASE_URL}/tools", json=request_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    # Give the server a moment to start if needed
    print("Please make sure the MCP server is running at http://localhost:5000")
    print("Press Enter to continue with the tests...")
    input()
    
    # Run the tests
    test_word_management_api() 