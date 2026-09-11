# UI Testing Guide

## Sample Data for Testing

I've created sample data in `data/samples/ui_test_data.json` with 10 representative customer messages covering different intents:

### Test Messages

1. **Delivery Problem**: "@AmazonHelp that is not my apartment!!!!!!! This is the sending time!!!! Where is my package!!!!!!!!!!"
2. **Refund Inquiry**: "Erm @AmazonHelp I bought this item for £5.99... why am I only getting £1.67 back?!"
3. **Complaint**: "@115850 I have stopped ordering from your site, Amazon courier guys are very rude."
4. **Shipping Question**: "@115821 why do I pay for 2 day shipping and it's going on 4 days."
5. **Refund Request**: "Worst experience in shopping no product no refund , been 40 days."
6. **Prime Membership**: "@115850 Hi, prime was available for 599/- per year few days back. Can you remind me when it will be back?"
7. **Product Issue**: "@117634 How do i set it so my new dire HD 10 kindle wont download apps and movies i never asked it too?"
8. **Price Adjustment**: "@115830 Can I get a price adjustment?"
9. **Feedback**: "@115821 I want to leave feedback about my experience"
10. **Order Status**: "@115830 The tracking information hasn't updated"

## How to Test the UI

### Option 1: Full Stack (with PostgreSQL)

1. **Start PostgreSQL**:
   ```bash
   docker compose up postgres -d
   ```

2. **Set up environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Initialize database**:
   ```bash
   cd backend
   npx tsx src/db/seed.ts
   ```

4. **Start backend**:
   ```bash
   cd backend
   npm run dev
   ```

5. **Start frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

6. **Access UI**: Open `http://localhost:5173`

### Option 2: Backend API Testing (Simpler)

1. **Start backend only**:
   ```bash
   cd backend
   npm run dev
   ```

2. **Test API with Python script**:
   ```bash
   cd data/samples
   python test_api_examples.py
   ```

### Option 3: Manual API Testing

Use curl or Postman to test the API:

```bash
# Health check
curl http://localhost:3001/health

# Analyze a message
curl -X POST http://localhost:3001/api/v1/support/analyze \
  -H "Content-Type: application/json" \
  -d '{"message": "@AmazonHelp where is my package?"}'
```

## Expected API Response Format

```json
{
  "intent": "delivery_problem",
  "confidence": 0.85,
  "response": "I can help you track your package. Please provide your order number...",
  "escalate": false,
  "escalation_reason": null,
  "evidence": [
    {
      "conversation_id": "1748",
      "similar_message": "@AmazonHelp that is not my apartment!!!!!!!",
      "agent_response": "@116094 I'm so sorry! We'd like to make sure this is addressed..."
    }
  ],
  "latency_ms": 150
}
```

## Available Intents

The system can classify messages into these 9 intents:

- `general_inquiry` (99 examples in training data)
- `delivery_problem` (26 examples)
- `refund_request` (13 examples)
- `return_exchange` (9 examples)
- `prime_membership` (8 examples)
- `payment_issue` (8 examples)
- `account_access` (4 examples)
- `order_status` (3 examples)
- `product_issue` (1 example)

## Testing Different Scenarios

### Test Escalation Logic
Try messages that should escalate:
- Complex technical issues
- Angry/complaint messages
- Account access problems
- Unusual requests

### Test Auto-Handle
Try messages that should be auto-handled:
- Simple status questions
- Common inquiries
- Clear intent with good evidence

### Test Edge Cases
- Very short messages
- Very long messages
- Messages with URLs
- Messages in other languages
- Messages with emojis