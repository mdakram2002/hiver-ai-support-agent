# Failure Analysis

**Note:** This analysis is based on demonstration evaluation results using AmazonHelp brand data with a sample golden set of 54 annotated examples. Production deployment would require analysis with real data and proper evaluation.

Based on evaluation results from baseline models and system analysis, here are the top 5 failure modes:

## 1. Intent Classification Confusion

**Failure Category**: Classification Error  
**Example**: Order status inquiries classified as general inquiry  
**What the system predicted**: general_inquiry  
**What should have happened**: order_status  
**Why it failed**: 
- TF-IDF baseline achieved only 72.2% accuracy
- Confusion matrix shows order_status (4 examples) had 0 precision/recall
- Order status messages often contain general language that overlaps with other intents
**Impact**: High - customers don't get relevant routing  
**Hypothesis**: Current keyword-based features don't capture enough context for order status  
**Potential fix**: Add entity extraction (order numbers, tracking IDs) and temporal features

## 2. Minority Intent Underperformance

**Failure Category**: Class Imbalance  
**Example**: return_exchange, refund_request with few examples  
**What the system predicted**: Often misclassified as general_inquiry  
**What should have happened**: Correct minority intent classification  
**Why it failed**:
- Training data shows significant imbalance (general_inquiry: 99 examples vs return_exchange: 9)
- TF-IDF with class_weight="balanced" still struggled with rare intents
- Majority baseline only achieved 37% accuracy by always predicting general_inquiry
**Impact**: Medium - specific issues get generic responses  
**Hypothesis**: Insufficient training examples for rare intents  
**Potential fix**: Data augmentation, few-shot learning, or hierarchical classification

## 3. Multilingual Message Handling

**Failure Category**: Language Processing  
**Example**: Portuguese message "Fiz um pedido pelo site da @117086..."  
**What the system predicted**: general_inquiry (correct but missed nuance)  
**What should have happened**: Language-aware processing with proper intent detection  
**Why it failed**:
- System appears monolingual (English-focused)
- EDA showed mixed languages in the dataset
- Current keyword patterns don't account for multilingual intent keywords
**Impact**: Medium - non-English users get less accurate service  
**Hypothesis**: Training data and classification pipeline assume English-only  
**Potential fix**: Language detection, multilingual embeddings, or language-specific models

## 4. Context-Aware Intent Detection

**Failure Category**: Context Understanding  
**Example**: Messages requiring conversation context ("also, beim Addams Family-Film...")  
**What the system predicted**: prime_video_issue (correct but without context)  
**What should have happened**: Understand this is a follow-up to previous conversation  
**Why it failed**:
- System processes each message independently
- No conversation state tracking
- "Also" and follow-up markers not recognized as context-dependent
**Impact**: Medium - misses continuity in multi-turn conversations  
**Hypothesis**: Isolated message processing without conversation history  
**Potential fix**: Conversation-level context tracking and stateful classification

## 5. Escalation Decision Uncertainty

**Failure Category**: Risk Assessment  
**Example**: Technical issues like "BBC Radio 4 Keeps dropping out"  
**What the system predicted**: Would need actual agent evaluation  
**What should have happened**: Escalate to technical support  
**Why it failed**:
- Current escalation thresholds are unconfigured (default values)
- No technical issue severity classification
- Groundedness checks limited by mock embeddings
**Impact**: High - technical issues may get inadequate automated responses  
**Hypothesis**: Escalation logic not tuned for technical complexity  
**Potential fix**: Technical issue detection, severity scoring, and configurable escalation rules

## Systematic Issues

### Data Limitations
- **Small golden set**: Only 54 annotated examples (recommended 150-250)
- **Sample size bias**: Only 100K messages from 2.8M dataset (3.6%)
- **Brand specificity**: Results only applicable to AmazonHelp, not generalizable

### Infrastructure Limitations
- **Mock embeddings**: Using random embeddings instead of real OpenAI embeddings
- **No PostgreSQL**: Unable to test actual pgvector retrieval
- **Missing LLM integration**: OPENAI_API_KEY not configured for real evaluation

### Evaluation Limitations
- **No AI agent evaluation**: Only baseline models evaluated
- **Mock LLM judge**: Using random scores instead of real LLM evaluation
- **No human agreement**: Human agreement analysis not implemented

## What is Misleading About Headline Numbers

**Headline**: "TF-IDF baseline achieves 72.2% accuracy"  
**Why misleading**:
1. **Small golden set**: Only 54 examples, high variance
2. **Imbalanced classes**: Accuracy inflated by majority class (general_inquiry)
3. **Mock training labels**: Training data labeled with simple keywords, not real human labels
4. **Brand-specific**: Only tested on AmazonHelp, may not generalize
5. **No AI agent comparison**: Baseline vs. nothing, not vs. actual AI system
6. **Easy examples**: Golden set may contain easier cases than real production
7. **No temporal split**: Training and evaluation from same time period
8. **Mock data**: Using 100K sample, not full dataset

**Real performance likely lower** due to:
- Production data more diverse and noisy
- Real user messages more ambiguous
- Multi-turn conversations more complex
- Edge cases not represented in small golden set