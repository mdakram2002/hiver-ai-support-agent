"""Simple backend server for UI testing without PostgreSQL."""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
import random
import urllib.parse

# Load sample data
sample_file = Path(__file__).parent / "ui_test_data.json"
with open(sample_file) as f:
    data = json.load(f)

def classify_message(message):
    """Simple keyword-based classification."""
    message_lower = message.lower()
    
    # Define intent patterns
    patterns = {
        'delivery_problem': ['package', 'delivery', 'delivered', 'where is my', 'shipping'],
        'refund_request': ['refund', 'money back', 'charge', 'billing'],
        'return_exchange': ['return', 'exchange', 'send back'],
        'prime_membership': ['prime', 'membership'],
        'product_issue': ['kindle', 'device', 'download', 'broken', 'damaged'],
        'order_status': ['order status', 'track my', 'tracking'],
        'payment_issue': ['payment', 'credit card', 'charged'],
        'account_access': ['password', 'log in', 'account'],
    }
    
    # Check for matches
    for intent, keywords in patterns.items():
        if any(keyword in message_lower for keyword in keywords):
            confidence = random.uniform(0.75, 0.95)
            return intent, confidence
    
    # Default to general_inquiry
    return 'general_inquiry', random.uniform(0.65, 0.85)

def get_evidence(intent, message):
    """Get similar examples from sample data."""
    matching_examples = [
        example for example in data['sample_messages']
        if example['expected_intent'] == intent
    ]
    
    if matching_examples:
        example = random.choice(matching_examples)
        return [{
            "conversationId": str(example['id']),
            "customerMessage": example['message'],
            "agentResponse": example['sample_response'],
            "intent": intent,
            "similarity": random.uniform(0.7, 0.9)
        }]
    return []

def generate_response(intent, message):
    """Generate a response based on intent."""
    responses = {
        'delivery_problem': "I can help you track your package. Please provide your order number so I can check the status and location of your delivery.",
        'refund_request': "I understand you're concerned about your refund. Let me help you check the status and resolve any issues with your refund process.",
        'general_inquiry': "I'd be happy to help you with your inquiry. Could you please provide more details about what you need assistance with?",
        'prime_membership': "I'd be happy to help with Prime membership questions. Current promotions and pricing vary, but I can check the latest offers for you.",
        'product_issue': "This sounds like a device settings issue. Let me help you troubleshoot the problem with your device.",
        'order_status': "I can help you check your order status. Please provide your order number so I can look into this for you.",
        'payment_issue': "I understand you have a payment concern. Let me help you review your charges and resolve any billing issues.",
        'return_exchange': "I can help you with your return or exchange. Please provide your order number and let me know what you'd like to return.",
        'account_access': "I can help you with account access issues. Let me assist you with logging in or resetting your password."
    }
    
    return responses.get(intent, responses['general_inquiry'])

def should_escalate(intent, confidence):
    """Determine if message should be escalated."""
    # Escalate if confidence is low or for certain intents
    high_risk_intents = ['product_issue', 'account_access', 'payment_issue']
    
    if confidence < 0.7:
        return True, "Low confidence in classification"
    if intent in high_risk_intents:
        return True, f"{intent} requires human review for security/complexity"
    
    return False, None

class SimpleHandler(BaseHTTPRequestHandler):
    def _set_cors_headers(self):
        """Set CORS headers for all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
    
    def _send_json_response(self, status_code, data):
        """Send JSON response with CORS headers."""
        self.send_response(status_code)
        self._set_cors_headers()
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS."""
        self.send_response(200)
        self._set_cors_headers()
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self._send_json_response(200, {
                "status": "healthy",
                "brand": data['metadata']['brand'],
                "total_pairs": data['metadata']['total_pairs']
            })
        elif self.path == '/api/v1/evaluation/results':
            self._send_json_response(200, {
                "golden_set_size": 54,
                "training_size": 43920,
                "tfidf": {
                    "accuracy": 0.722,
                    "macro_f1": 0.626
                },
                "majority": {
                    "accuracy": 0.370,
                    "macro_f1": 0.049
                }
            })
        else:
            self._send_json_response(404, {"error": "Not found"})
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/api/v1/support/analyze':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8'))
                
                message = payload.get('message', '')
                
                if not message:
                    self._send_json_response(400, {"error": "Message is required"})
                    return
                
                # Classify the message
                intent, confidence = classify_message(message)
                
                # Get evidence
                evidence = get_evidence(intent, message)
                
                # Generate response
                response = generate_response(intent, message)
                
                # Determine escalation
                should_escalate_flag, escalation_reason = should_escalate(intent, confidence)
                
                # Build result
                result = {
                    "intent": {
                        "name": intent,
                        "confidence": confidence,
                        "uncertain": confidence < 0.7
                    },
                    "reply": response,
                    "escalation": {
                        "shouldEscalate": should_escalate_flag,
                        "reason": escalation_reason
                    },
                    "evidence": evidence,
                    "metadata": {
                        "retrievalCount": len(evidence),
                        "latencyMs": random.randint(50, 200)
                    }
                }
                
                self._send_json_response(200, result)
                
            except Exception as e:
                self._send_json_response(500, {"error": str(e)})
        else:
            self._send_json_response(404, {"error": "Not found"})

def run_server():
    """Run the simple HTTP server."""
    server_address = ('', 3001)
    httpd = HTTPServer(server_address, SimpleHandler)
    
    print("=== Simple Backend Server ===")
    print(f"Brand: {data['metadata']['brand']}")
    print(f"Total resolution pairs: {data['metadata']['total_pairs']}")
    print("Server running on http://localhost:3001")
    print("Press Ctrl+C to stop")
    print()
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

if __name__ == '__main__':
    run_server()