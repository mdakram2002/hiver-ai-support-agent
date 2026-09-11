"""Label resolution pairs with intents based on customer message content."""

import argparse
import json
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="../../data/processed/resolution_pairs.csv")
    parser.add_argument("--taxonomy", default="../../data/processed/intent_taxonomy.json")
    parser.add_argument("--output", default="../../data/processed/resolution_pairs_labeled.csv")
    args = parser.parse_args()
    
    # Load resolution pairs
    df = pd.read_csv(args.input)
    print(f"Loaded {len(df)} resolution pairs")
    
    # Load intent taxonomy
    with open(args.taxonomy, 'r', encoding='utf-8') as f:
        taxonomy = json.load(f)
    
    intents = taxonomy['intents']
    intent_mapping = {intent['name']: intent for intent in intents}
    print(f"Loaded {len(intents)} intents from taxonomy")
    
    # Simple keyword-based labeling for demonstration
    # In production, this would use LLM-based classification
    def classify_message(text):
        text_lower = text.lower()
        
        # Define keyword patterns for each intent
        patterns = {
            'order_status': ['where is my order', 'order status', 'delivery status', 'when will', 'track my', 'shipping status'],
            'refund_request': ['refund', 'money back', 'get my money', 'refund my'],
            'return_exchange': ['return', 'exchange', 'send back', 'replace'],
            'payment_issue': ['charged twice', 'charge', 'payment', 'billing', 'credit card'],
            'account_access': ['log in', 'password', 'account', 'access', 'login'],
            'product_issue': ['damaged', 'broken', 'defective', 'does not work', 'wrong item', 'not working'],
            'prime_video_issue': ['prime video', 'streaming', 'video not', 'playback', 'tunein'],
            'delivery_problem': ['not delivered', 'delivery', 'package', 'left at', 'delivered but'],
            'prime_membership': ['prime', 'membership', 'prime student', 'cancel prime'],
            'general_inquiry': ['question', 'help', 'how do i', 'can i', 'information', 'customer service']
        }
        
        # Check for matches
        for intent, keywords in patterns.items():
            if any(keyword in text_lower for keyword in keywords):
                return intent
        
        # Default to general_inquiry if no match
        return 'general_inquiry'
    
    # Apply classification
    df['intent'] = df['customer_message'].apply(classify_message)
    
    # Print distribution
    intent_counts = df['intent'].value_counts()
    print("Intent distribution:")
    for intent, count in intent_counts.items():
        print(f"  {intent}: {count}")
    
    # Save labeled pairs
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"Saved labeled pairs to {args.output}")
    
    # Save labeling metadata
    metadata = {
        "total_pairs": len(df),
        "intents_used": list(intent_counts.keys()),
        "intent_distribution": {str(k): int(v) for k, v in intent_counts.items()},
        "labeling_method": "keyword-based for demonstration",
        "taxonomy_source": str(args.taxonomy)
    }
    
    metadata_path = Path(args.output).parent / "labeling_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Saved labeling metadata to {metadata_path}")


if __name__ == "__main__":
    main()