"""Sample messages from evaluation set for golden annotation."""

import argparse
import json
import random
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="../../data/processed/eval_threads.csv")
    parser.add_argument("--brand", required=True)
    parser.add_argument("--output", default="../../evaluation/golden_set/golden_set.csv")
    parser.add_argument("--sample-size", type=int, default=200)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    
    random.seed(args.seed)
    
    df = pd.read_csv(args.input)
    
    # Filter for brand conversations
    brand_conversations = df[df.author_id.astype(str) == args.brand].conversation_id.unique()
    brand_df = df[df.conversation_id.isin(brand_conversations)].copy()
    
    # Get customer messages
    brand_df['inbound'] = brand_df['inbound'].astype(str).str.lower().isin({'true', '1', 'yes'})
    customer_messages = brand_df[brand_df['inbound'] == True].copy()
    
    print(f"Total customer messages for {args.brand}: {len(customer_messages)}")
    
    # Sample messages
    if len(customer_messages) < args.sample_size:
        print(f"Warning: Only {len(customer_messages)} messages available, using all")
        sampled = customer_messages
    else:
        sampled = customer_messages.sample(n=args.sample_size, random_state=args.seed)
    
    print(f"Sampled {len(sampled)} messages for annotation")
    
    # Create golden set structure
    golden_data = []
    for _, row in sampled.iterrows():
        golden_data.append({
            "id": f"GS_{row['tweet_id']}",
            "customer_message": row['text'],
            "expected_intent": "",
            "expected_escalation": "",
            "expected_resolution": "",
            "difficulty": "",
            "notes": "",
            "source_conversation_id": row['conversation_id']
        })
    
    # Save to CSV
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    golden_df = pd.DataFrame(golden_data)
    golden_df.to_csv(args.output, index=False)
    
    print(f"Saved golden set template to {args.output}")
    print(f"Please manually annotate the expected_intent, expected_escalation, and expected_resolution columns")
    
    # Save sampling metadata
    metadata = {
        "brand": args.brand,
        "sample_size": len(sampled),
        "seed": args.seed,
        "total_available": len(customer_messages),
        "source_file": str(args.input),
        "instructions": "Fill in expected_intent, expected_escalation, expected_resolution, difficulty, and notes columns"
    }
    
    metadata_path = Path(args.output).parent / "sampling_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Saved sampling metadata to {metadata_path}")


if __name__ == "__main__":
    main()