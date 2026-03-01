import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"
API_KEY = "your-super-secret-key"  # Default from config.py

def test_ask_auth():
    payload = {"question": "What is RAG?"}
    
    # 1. Test without header
    print("Test 1: Missing Header")
    try:
        response = requests.post(f"{BASE_URL}/ask", json=payload)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

    # 2. Test with wrong key
    print("Test 2: Wrong API Key")
    try:
        response = requests.post(
            f"{BASE_URL}/ask", 
            json=payload, 
            headers={"X-Internal-API-Key": "wrong-key"}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

    # 3. Test with correct key
    # Note: This might fail if the server isn't running or ChromaDB isn't accessible,
    # but the status code should tell us if the AUTH passed.
    print("Test 3: Correct API Key")
    try:
        response = requests.post(
            f"{BASE_URL}/ask", 
            json=payload, 
            headers={"X-Internal-API-Key": API_KEY}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Auth Success!")
        else:
            print(f"Auth likely passed but backend error: {response.status_code}")
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ask_auth()
