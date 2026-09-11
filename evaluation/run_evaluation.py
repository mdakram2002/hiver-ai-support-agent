"""Run only after a real, isolated golden set and train data are available."""

import json
import warnings
from pathlib import Path
import pandas as pd
from baselines.majority_baseline import predict as majority
from baselines.tfidf_baseline import predict as tfidf
from metrics.classification import classification_metrics

warnings.filterwarnings("ignore")

root = Path(__file__).parent
golden = root / "golden_set/golden_set_annotated.csv"
train = root.parent / "data/processed/train_threads.csv"

if not golden.exists():
    raise SystemExit(
        "Not evaluated: create human-labelled golden_set_annotated.csv first."
    )

if not train.exists():
    raise SystemExit(
        "Not evaluated: create leakage-safe train_threads.csv first."
    )

g = pd.read_csv(golden)
t = pd.read_csv(train)

# Filter golden set to only include labeled examples
g = g[g['expected_intent'] != ''].copy()

if len(g) < 150 or len(g) > 250:
    print(f"Warning: Golden set has {len(g)} examples (recommended: 150–250)")

print(f"Running evaluation on {len(g)} golden set examples")
print(f"Training data: {len(t)} messages")

# Prepare training data for baselines (customer messages only)
t['inbound'] = t['inbound'].astype(str).str.lower().isin({'true', '1', 'yes'})
train_messages = t[t['inbound'] == True].copy()

# Rename columns to match expected format
train_messages = train_messages.rename(columns={'text': 'customer_message'})

# Create labels for training data (use keyword-based classification for demo)
def classify_for_training(text):
    text_lower = text.lower()
    patterns = {
        'order_status': ['where is my order', 'order status', 'delivery status', 'when will', 'track my'],
        'refund_request': ['refund', 'money back', 'get my money'],
        'return_exchange': ['return', 'exchange', 'send back'],
        'payment_issue': ['charged twice', 'charge', 'payment', 'billing'],
        'account_access': ['log in', 'password', 'account', 'access'],
        'product_issue': ['damaged', 'broken', 'defective', 'does not work'],
        'prime_video_issue': ['prime video', 'streaming', 'video not'],
        'delivery_problem': ['not delivered', 'delivery', 'package'],
        'prime_membership': ['prime', 'membership', 'prime student'],
        'general_inquiry': ['question', 'help', 'how do i', 'can i']
    }
    for intent, keywords in patterns.items():
        if any(keyword in text_lower for keyword in keywords):
            return intent
    return 'general_inquiry'

train_messages['intent'] = train_messages['customer_message'].apply(classify_for_training)

print(f"Training messages with labels: {len(train_messages)}")

out = {
    "golden_set_size": len(g),
    "training_size": len(train_messages),
    "majority": classification_metrics(g.expected_intent, majority(train_messages, g)),
    "tfidf": classification_metrics(g.expected_intent, tfidf(train_messages, g)),
}

results_path = root.parent / "reports/evaluation_results.json"
results_path.parent.mkdir(parents=True, exist_ok=True)
results_path.write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
print(f"Results saved to {results_path}")
