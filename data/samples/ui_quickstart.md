# UI Quickstart Guide

## Option 1: Standalone HTML Test (Fastest - No Backend Required)

This is the easiest way to test the UI immediately:

1. **Open the test page in your browser:**
   ```
   data/samples/frontend_test.html
   ```

2. **Test with sample messages:**
   - Click any of the sample message buttons
   - Or type your own message in the text area
   - Click "Analyze Message"

3. **See results:**
   - Intent classification with confidence score
   - Escalation decision (YES/NO)
   - Generated response
   - Similar historical evidence
   - Response latency

**No server required!** This uses mock responses locally in your browser.

---

## Option 2: Simple Python Backend (Recommended)

If you want to test with the actual React frontend:

### Step 1: Start the Simple Backend

**Windows:**
```bash
# Double-click this file:
data/samples/start_simple_backend.bat

# Or run manually:
cd data/samples
python simple_backend_server.py
```

**Mac/Linux:**
```bash
cd data/samples
python simple_backend_server.py
```

You should see:
```
=== Simple Backend Server ===
Brand: AmazonHelp
Total resolution pairs: 171
Server running on http://localhost:3001
Press Ctrl+C to stop
```

### Step 2: Start the React Frontend

In a new terminal:
```bash
cd frontend
npm run dev
```

### Step 3: Open the UI

Open your browser to: `http://localhost:5173`

### Step 4: Test the UI

1. **Enter a customer message** in the text area, for example:
   - "@AmazonHelp where is my package?"
   - "I want a refund for my order"
   - "Hi, prime was available for 599/- per year few days back"

2. **Click "Analyze message"**

3. **See results in the "AI analysis" panel:**
   - Intent classification (e.g., "delivery_problem")
   - Confidence score (e.g., 0.85)
   - Escalation decision (YES/NO with reason)
   - Generated response
   - Similar historical evidence
   - Performance metrics

---

## Option 3: Full Stack with PostgreSQL (Complete System)

If you want to test the complete system with real database:

### Step 1: Start PostgreSQL
```bash
docker compose up postgres -d
```

### Step 2: Set up environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### Step 3: Initialize database
```bash
cd backend
npx tsx src/db/seed.ts
```

### Step 4: Start backend
```bash
cd backend
npm run dev
```

### Step 5: Start frontend
```bash
cd frontend
npm run dev
```

### Step 6: Open UI
Open `http://localhost:5173` in your browser

---

## Sample Messages to Try

Here are some good test messages:

**Delivery Issues:**
- "@AmazonHelp that is not my apartment!!!!!!! This is the sending time!!!! Where is my package!!!!!!!!!!"
- "@115821 why do I pay for 2 day shipping and it's going on 4 days."

**Refund/Return:**
- "Erm @AmazonHelp I bought this item for £5.99... why am I only getting £1.67 back?!"
- "Worst experience in shopping no product no refund , been 40 days."

**Prime Membership:**
- "@115850 Hi, prime was available for 599/- per year few days back. Can you remind me when it will be back?"

**Product Issues:**
- "@117634 How do i set it so my new dire HD 10 kindle wont download apps and movies i never asked it too?"

**General Inquiries:**
- "@115830 Can I get a price adjustment?"
- "@115821 I want to leave feedback about my experience"

---

## Troubleshooting

**Backend not starting:**
- Make sure port 3001 is not already in use
- Check that Python is installed: `python --version`

**Frontend not starting:**
- Make sure you're in the `frontend` directory
- Run `npm install` if dependencies are missing

**UI shows errors:**
- Check that the backend is running on http://localhost:3001
- Open browser console (F12) to see error messages

**CORS errors:**
- The simple backend server includes CORS headers
- If using full stack, check backend CORS configuration

---

## Expected Response Format

When you analyze a message, you should see:

```json
{
  "intent": {
    "name": "delivery_problem",
    "confidence": 0.85,
    "uncertain": false
  },
  "reply": "I can help you track your package...",
  "escalation": {
    "shouldEscalate": false,
    "reason": null
  },
  "evidence": [
    {
      "conversationId": "1748",
      "customerMessage": "@AmazonHelp that is not my apartment...",
      "agentResponse": "@116094 I'm so sorry!...",
      "intent": "delivery_problem",
      "similarity": 0.82
    }
  ],
  "metadata": {
    "retrievalCount": 1,
    "latencyMs": 120
  }
}
```

---

## Quick Test Commands

**Test API directly:**
```bash
# Health check
curl http://localhost:3001/health

# Analyze a message
curl -X POST http://localhost:3001/api/v1/support/analyze \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"@AmazonHelp where is my package?\"}"
```

**Test with Python:**
```bash
cd data/samples
python simple_backend_test.py
```