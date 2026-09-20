# Report — Customer Support AI Agent

## Problem framing

For this project, I defined "good" as a support agent that can: (1) accurately classify customer messages into a manageable set of intents, (2) retrieve historically relevant resolutions to ground responses, and (3) make safe escalation decisions when uncertain. I explicitly chose not to build policy automation, account actions, or open-ended chatbot behavior - I focused on the core classification and evidence-grounded response problem.

## Dataset and brand

I used the Kaggle Customer Support on Twitter dataset and selected AmazonHelp as my brand. I chose AmazonHelp because it had sufficient conversation volume (586 customer messages in my sample), clear customer-agent interaction patterns, and diverse issue types. I worked with a 100K tweet sample from the full 3M dataset to enable faster iteration while maintaining enough data for meaningful analysis.

## System and evaluation design

My system uses a structured-output classifier constrained to a taxonomy I developed from the data, vector similarity search over historical resolution pairs, evidence-constrained response drafting, and deterministic escalation based on confidence thresholds. For evaluation, I created a 54-example golden set isolated from training data and compared against two baselines: a trivial majority classifier and a TF-IDF + logistic regression model. I implemented an LLM-as-judge rubric with five dimensions (groundedness, relevance, helpfulness, completeness, tone) for response quality assessment.

## Results

My evaluation shows that even simple ML approaches significantly outperform trivial baselines:

- **TF-IDF baseline:** 72.2% accuracy, 0.63 macro F1, 0.67 weighted F1
- **Majority baseline:** 37.0% accuracy, 0.05 macro F1, 0.20 weighted F1
- **My taxonomy:** 10 intents developed from AmazonHelp data, with general_inquiry being most common (37% of golden set)
- **LLM judge scores:** Groundedness 4.13/5, Relevance 4.09/5, Helpfulness 3.98/5, Completeness 3.94/5, Tone 4.54/5

The 35-point accuracy improvement from majority to TF-IDF shows there's meaningful signal in the text data. However, macro F1 of 0.63 indicates the system struggles with rare intents - a classic class imbalance problem I discuss in the failure analysis.

## Failure analysis

I analyzed my evaluation results and identified these top 5 failure modes:

1. **Intent Classification Confusion**: Order status messages (4 examples) had 0 precision/recall because they contain general language overlapping with other intents. Fix: Add entity extraction for order numbers and tracking IDs.

2. **Minority Intent Underperformance**: Return_exchange (9 training examples) and refund_request (13 examples) get misclassified as general_inquiry due to class imbalance. Fix: Data augmentation or few-shot learning for rare intents.

3. **Multilingual Handling**: Portuguese messages like "Fiz um pedido pelo site da @117086..." get correct classification but miss nuance. Fix: Language detection and multilingual embeddings.

4. **Context-Aware Detection**: Messages with follow-up markers like "also" don't capture conversation continuity. Fix: Conversation-level context tracking.

5. **Escalation Uncertainty**: Technical issues like "BBC Radio 4 Keeps dropping out" need specialized handling but escalation thresholds are unconfigured. Fix: Technical issue detection and severity scoring.

## What is misleading about my headline number?

My headline number is "TF-IDF achieves 72.2% accuracy." Here's why this is misleading:

1. **Small golden set**: Only 54 examples vs recommended 150-250, so variance is high
2. **Class imbalance**: Accuracy inflated by majority class (general_inquiry is 37% of data)
3. **Mock training labels**: I used keyword-based classification for training data, not human labels
4. **Brand-specific**: Only tested on AmazonHelp, may not generalize to other brands
5. **No AI agent comparison**: I compared baselines against each other, not against my actual system
6. **No retrieval evaluation**: I haven't measured how well the vector search finds relevant resolutions
7. **Same time period**: Training and evaluation from same time period, no temporal split
8. **Sample bias**: 100K sample from 3M dataset may not represent full distribution

Real production performance would likely be lower due to noisier data, more ambiguous messages, and edge cases not represented in my small golden set.

## One more week

With one more week, I would: (1) expand the golden set to 200+ examples with dual annotation for reliability, (2) implement real OpenAI embeddings instead of dummy vectors, (3) add a retrieval baseline to measure search quality, (4) test threshold calibration on a development split, (5) add retrieval relevance labels, (6) audit for retrieval leakage, (7) collect latency/cost distributions, and (8) manually review the highest-risk false auto-handles to understand failure patterns.