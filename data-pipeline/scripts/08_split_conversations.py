"""Split conversations into train and evaluation sets with leakage protection."""

import argparse
import hashlib
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="../../data/processed/threads.csv")
    parser.add_argument("--train-output", default="../../data/processed/train_threads.csv")
    parser.add_argument("--eval-output", default="../../data/processed/eval_threads.csv")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--eval-ratio", type=float, default=0.2)
    args = parser.parse_args()
    
    df = pd.read_csv(args.input)
    print(f"Loaded {len(df)} messages from {df['conversation_id'].nunique()} conversations")
    
    # Get unique conversation IDs
    unique_conversations = df['conversation_id'].unique()
    print(f"Unique conversations: {len(unique_conversations)}")
    
    # Deterministic split using hash of conversation ID
    def hash_to_split(conv_id):
        hash_val = int(hashlib.md5(str(conv_id).encode()).hexdigest(), 16)
        return hash_val % 100 < (args.eval_ratio * 100)
    
    # Split conversations
    eval_conversations = set(conv_id for conv_id in unique_conversations if hash_to_split(conv_id))
    train_conversations = set(unique_conversations) - eval_conversations
    
    print(f"Train conversations: {len(train_conversations)}")
    print(f"Eval conversations: {len(eval_conversations)}")
    
    # Split the dataframe
    train_df = df[df['conversation_id'].isin(train_conversations)].copy()
    eval_df = df[df['conversation_id'].isin(eval_conversations)].copy()
    
    print(f"Train messages: {len(train_df)}")
    print(f"Eval messages: {len(eval_df)}")
    
    # Verify no leakage
    overlap = set(train_df['conversation_id'].unique()) & set(eval_df['conversation_id'].unique())
    if overlap:
        raise ValueError(f"Conversation leakage detected: {overlap}")
    else:
        print("No conversation leakage between train and eval sets")
    
    # Save splits
    Path(args.train_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.eval_output).parent.mkdir(parents=True, exist_ok=True)
    
    train_df.to_csv(args.train_output, index=False)
    eval_df.to_csv(args.eval_output, index=False)
    
    print(f"Saved train set to {args.train_output}")
    print(f"Saved eval set to {args.eval_output}")
    
    # Save split metadata
    metadata = {
        "seed": args.seed,
        "eval_ratio": args.eval_ratio,
        "total_conversations": len(unique_conversations),
        "train_conversations": len(train_conversations),
        "eval_conversations": len(eval_conversations),
        "total_messages": len(df),
        "train_messages": len(train_df),
        "eval_messages": len(eval_df),
        "leakage_check": "PASSED - no overlapping conversation IDs"
    }
    
    import json
    metadata_path = Path(args.train_output).parent / "split_metadata.json"
    metadata_path.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Saved split metadata to {metadata_path}")


if __name__ == "__main__":
    main()