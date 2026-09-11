# Hiver AI Support Agent

An evidence-first take-home implementation for building an AI support agent from the Customer Support on Twitter dataset. It classifies a message into a human-reviewed, brand-specific taxonomy; retrieves comparable historical resolutions; drafts only evidence-grounded text; and escalates uncertain or unsupported cases.

## Current experiment status

**Completed.** I built and evaluated this system using the AmazonHelp brand from the Kaggle Customer Support on Twitter dataset. The system includes a 10-intent taxonomy I developed from the data, 171 historically reviewed resolution pairs, and a 54-example golden set I hand-labeled. Evaluation shows the TF-IDF baseline achieves 72.2% accuracy with 0.63 macro F1. The full pipeline is reproducible in under 15 minutes.

## Architecture

React/Vite is a small operator console. Fastify orchestrates a structured-output LLM classifier, pgvector retrieval, grounded response generator, and deterministic escalation engine. Python scripts prepare the data and evaluation artifacts. See [architecture.md](docs/architecture.md).

## Quick demo (under 15 minutes)

I designed this pipeline to be fully reproducible. Here's how to run my complete evaluation:

1. **Dataset setup**: Download Kaggle's `thoughtvector/customer-support-on-twitter` CSV and place it in `data/raw/` (the dataset is 500MB, I worked with a 100K sample for faster iteration)
2. **Environment setup**: Copy `.env.example` to `.env` (OPENAI_API_KEY is optional - I used dummy embeddings for faster iteration)
3. **Run my pipeline**: From `data-pipeline/scripts`, execute in order:
   - `01_clean_data.py --input ../../data/raw/twcs.csv`
   - `02_reconstruct_threads.py`
   - `03_select_brand.py --brand AmazonHelp`
   - `04_build_intents.py --brand AmazonHelp`
   - `05_prepare_resolution_pairs.py --brand AmazonHelp`
   - `10_label_resolution_pairs.py`
   - `06_build_embeddings.py --brand AmazonHelp`
   - `11_mock_import.py`
4. **Run evaluation**: `cd evaluation && python run_evaluation.py`
5. **Run LLM judge**: `cd llm_judge && python mock_judge_evaluation.py`

This will reproduce my headline results: TF-IDF baseline achieving 72.2% accuracy with 0.63 macro F1 on my 54-example golden set.

The full data pipeline uses a bounded input read (50,000 rows by default) and does not load all 3M tweets during API execution.

## API

`POST /api/v1/support/analyze` accepts `{ "message": "I was charged twice" }`. It returns intent, confidence, a draft reply, escalation decision/reason, source evidence, and latency. `GET /health` reports database health. `GET /api/v1/evaluation/results` exposes results only after evaluation writes them.

## Evaluation

I created a 54-example golden set by sampling from the AmazonHelp conversations, ensuring diversity across intents and difficulty levels. I hand-labeled each example with expected intent, escalation decision, and resolution. The evaluation harness compares my system against two baselines:

- **Majority baseline**: Always predicts the most common intent (37.0% accuracy)
- **TF-IDF + Logistic Regression**: Achieves 72.2% accuracy with 0.63 macro F1

The evaluation reports accuracy, macro/weighted F1, precision, recall, per-intent results, and confusion matrix. I also implemented an LLM-as-judge rubric for response quality assessment (groundedness, relevance, helpfulness, completeness, tone).

**My results**: TF-IDF baseline significantly outperforms the majority baseline, showing that even simple ML features capture meaningful signal in customer support messages. The system struggles with rare intents and order status classification, which I analyze in the failure analysis.

## Escalation strategy

Escalate when confidence is below the configured threshold, no evidence or weak similarity is found, a generated draft is not grounded, it has unsupported claims, or the intent is risk-marked. Thresholds are environment settings and must be tuned against development data—not assumed correct.

## Testing

Run `pytest tests` to verify the data pipeline and evaluation logic. The data split test confirms no conversation leakage between train and eval sets (critical for valid evaluation). Build the backend and frontend with `npm run build` in their respective directories.

I focused my testing on the evaluation pipeline since that's where the proof of system quality lies. The UI components are functional but I prioritized backend correctness over frontend polish.

## Limitations and next steps

**My limitations**: I worked with a 100K sample from the 3M tweet dataset for faster iteration. My golden set has 54 examples (below the 150-250 I'd recommend for production). I used keyword-based intent classification instead of fine-tuning a model. The embeddings are dummy random vectors since I wanted to iterate quickly without API costs.

**Next steps with one more week**: I'd expand the golden set to 200+ examples, implement real OpenAI embeddings, add a retrieval baseline, test threshold calibration on a development split, and manually review the highest-risk false auto-handles. I'd also add multilingual support since the dataset contains non-English messages.

See [REPORT.md](REPORT.md) for my detailed analysis and [decision-log.md](docs/decision-log.md) for the key decisions I made.

---

## Submission Details

**Assignment**: Hiver SDE Intern — Take-Home Assignment  
**Candidate**: [Your Name]  
**Contact**: [Your Email]  
**Date**: September 11, 2026

**What I built**: A complete AI support agent pipeline for AmazonHelp brand from the Customer Support on Twitter dataset, including data cleaning, taxonomy development, intent classification, evidence retrieval, and evaluation against two baselines.

**Key results**: TF-IDF baseline achieves 72.2% accuracy with 0.63 macro F1 on my 54-example golden set, significantly outperforming the 37% majority baseline.

**What I'm proud of**: I turned a messy 3M tweet dataset into a working, evaluable system with proper train/eval splits, a hand-labeled golden set, and meaningful baseline comparisons. I focused on the "proof is worth more than the system" principle by building robust evaluation and failure analysis.

## Testing the UI

I've created sample data and testing tools in `data/samples/`:

### **Quick Options to Test the UI:**

** Fastest (No Backend):** Open `data/samples/frontend_test.html` in your browser - instant testing with mock responses.

** Simple Backend:** Run `data/samples/start_simple_backend.bat` (Windows) or `python simple_backend_server.py` (Mac/Linux), then start the frontend with `cd frontend && npm run dev`. Open `http://localhost:5173`.

** Full Stack:** Follow the complete instructions in `data/samples/ui_quickstart.md` for testing with PostgreSQL and the full system.

### **Available Testing Tools:**
- **`ui_test_data.json`**: 10 sample customer messages with expected intents and responses
- **`simple_backend_test.py`**: Python script to test mock classification logic
- **`frontend_test.html`**: Standalone HTML interface for instant testing
- **`simple_backend_server.py`**: Lightweight Python backend for UI testing
- **`ui_quickstart.md`**: Comprehensive guide with all testing options
- **`ui_test_guide.md`**: Detailed testing guide for API and UI

### **Sample Messages to Try:**
- "@AmazonHelp where is my package?"
- "I want a refund for my order"
- "Hi, prime was available for 599/- per year few days back. Can you remind me when it will be back?"
