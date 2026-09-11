"""Simple backend test without database dependencies."""

import json
from pathlib import Path

# Mock data for testing when database is not available
MOCK_RESPONSES = {
    "delivery_problem": {
        "intent": "delivery_problem",
        "confidence": 0.85,
        "response": "I can help you track your package. Please provide your order number so I can check the status and location of your delivery.",
        "escalate": False,
        "escalation_reason": None,
        "evidence": [
            {
                "conversation_id": "1748",
                "similar_message": "@AmazonHelp that is not my apartment!!!!!!! This is the sending time!!!! Where is my package!!!!!!!!!!",
                "agent_response": "@116094 I'm so sorry! We'd like to make sure this is addressed. Please provide some details here: https://t.co/KctVgMFvbp (1/2)"
            }
        ],
        "latency_ms": 120
    },
    "general_inquiry": {
        "intent": "general_inquiry",
        "confidence": 0.72,
        "response": "I'd be happy to help you with your inquiry. Could you please provide more details about what you need assistance with?",
        "escalate": False,
        "escalation_reason": None,
        "evidence": [
            {
                "conversation_id": "2561",
                "similar_message": "Erm @AmazonHelp I bought this item for £5.99... why am I only getting £1.67 back?!",
                "agent_response": "@116318 I'm sorry you didn't receive the refund amount you expected. Please check here for more info: https://t.co/I5rEOyBt2k ^BT"
            }
        ],
        "latency_ms": 95
    },
    "refund_request": {
        "intent": "refund_request",
        "confidence": 0.91,
        "response": "I understand you're concerned about your refund. Let me help you check the status and resolve any issues with your refund process.",
        "escalate": True,
        "escalation_reason": "Refund requests involving significant delays or amounts require human review",
        "evidence": [
            {
                "conversation_id": "9767",
                "similar_message": "Worst experience in shopping no product no refund , been 40 days.",
                "agent_response": "@117789 Apologies for the delay in delivery of your order, Benish. We'd like to take a closer look. 1/2 ^HD"
            }
        ],
        "latency_ms": 150
    }
}

def mock_classify_message(message):
    """Simple mock classification for testing."""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['package', 'delivery', 'delivered', 'where is my']):
        return MOCK_RESPONSES["delivery_problem"]
    elif any(word in message_lower for word in ['refund', 'money back']):
        return MOCK_RESPONSES["refund_request"]
    else:
        return MOCK_RESPONSES["general_inquiry"]

def main():
    """Test with sample messages."""
    print("=== Mock Backend Test ===\n")
    
    # Load sample data
    sample_file = Path(__file__).parent / "ui_test_data.json"
    with open(sample_file) as f:
        data = json.load(f)
    
    # Test a few messages
    test_messages = [
        data["sample_messages"][0],  # delivery problem
        data["sample_messages"][1],  # general inquiry  
        data["sample_messages"][4],  # refund request
    ]
    
    for i, test_case in enumerate(test_messages, 1):
        print(f"--- Test {i} ---")
        print(f"Message: {test_case['message'][:60]}...")
        print(f"Expected Intent: {test_case['expected_intent']}")
        
        result = mock_classify_message(test_case['message'])
        
        print(f"Predicted Intent: {result['intent']}")
        print(f"Confidence: {result['confidence']}")
        print(f"Escalate: {result['escalate']}")
        print(f"Response: {result['response'][:80]}...")
        print(f"Match: {'PASS' if result['intent'] == test_case['expected_intent'] else 'FAIL'}")
        print()
    
    print("=== Available Intents ===")
    for intent in data["available_intents"]:
        print(f"  - {intent}")
    
    print(f"\n=== Metadata ===")
    print(f"Brand: {data['metadata']['brand']}")
    print(f"Total Resolution Pairs: {data['metadata']['total_pairs']}")

if __name__ == "__main__":
    main()