"""Test API endpoints with sample data for UI demonstration."""

import json
import requests
from pathlib import Path

# Load sample data
sample_file = Path(__file__).parent / "ui_test_data.json"
with open(sample_file) as f:
    data = json.load(f)

BASE_URL = "http://localhost:3001"

def test_health():
    """Test health endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_support_analysis(message):
    """Test support analysis endpoint."""
    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/support/analyze",
            json={"message": message},
            headers={"Content-Type": "application/json"}
        )
        print(f"\nAnalysis Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"Intent: {result.get('intent')}")
            print(f"Confidence: {result.get('confidence')}")
            print(f"Escalate: {result.get('escalate')}")
            print(f"Response: {result.get('response')[:100]}...")
            return result
        else:
            print(f"Error: {response.text}")
            return None
    except Exception as e:
        print(f"Analysis failed: {e}")
        return None

def main():
    """Run API tests with sample data."""
    print("=== Customer Support AI Agent - API Test ===\n")
    
    # Test health
    if not test_health():
        print("Backend not available. Please start the backend first.")
        print("Run: cd backend && npm run dev")
        return
    
    # Test a few sample messages
    print("\n=== Testing Sample Messages ===")
    
    # Test different types of messages
    test_cases = [
        data["sample_messages"][0],  # delivery problem
        data["sample_messages"][1],  # general inquiry
        data["sample_messages"][4],  # refund request
        data["sample_messages"][6],  # product issue
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Message: {test_case['message'][:80]}...")
        print(f"Expected Intent: {test_case['expected_intent']}")
        
        result = test_support_analysis(test_case['message'])
        
        if result:
            print(f"✓ Analysis completed")
        else:
            print(f"✗ Analysis failed")
    
    print("\n=== Available Intents ===")
    for intent in data["available_intents"]:
        print(f"  - {intent}")
    
    print(f"\n=== Metadata ===")
    print(f"Brand: {data['metadata']['brand']}")
    print(f"Total Resolution Pairs: {data['metadata']['total_pairs']}")

if __name__ == "__main__":
    main()