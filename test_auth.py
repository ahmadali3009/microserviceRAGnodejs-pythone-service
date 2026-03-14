import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"
API_KEY = "your-super-secret-key"  # Default from config.py

def test_ask_auth():
    payload = {
        "question": "What is RAG?",
        "tenant_id": "default_tenant"  # Added this
    }
    
    # 1. Test without header
    print("Test 1: Missing Header")
    try:
        response = requests.post(f"{BASE_URL}/ask", json={"question": "What is RAG?"}) # Intentionally missing tenant_id to see 422
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

    # 2. Test with correct key but missing tenant_id
    print("Test 2: Missing tenant_id")
    try:
        response = requests.post(
            f"{BASE_URL}/ask", 
            json={"question": "What is RAG?"}, 
            headers={"X-Internal-API-Key": API_KEY}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    print("-" * 20)

    # 3. Test with correct key and correct payload
    print("Test 3: Correct API Key and Payload")
    try:
        response = requests.post(
            f"{BASE_URL}/ask", 
            json=payload, 
            headers={"X-Internal-API-Key": API_KEY}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("Success!")
            print(f"Response: {response.json().get('answer')[:100]}...")
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ask_auth()
