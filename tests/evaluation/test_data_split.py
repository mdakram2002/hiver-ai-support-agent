"""Test conversation-level split leakage protection."""

import pandas as pd
from pathlib import Path


def test_conversation_leakage():
    """Verify no conversation IDs overlap between train and eval sets."""
    # Try multiple possible path locations
    script_dir = Path(__file__).parent
    project_root = script_dir.parent.parent
    
    # Try relative path from tests/evaluation directory
    train_path = script_dir / "../../data/processed/train_threads.csv"
    eval_path = script_dir / "../../data/processed/eval_threads.csv"
    
    # If not found, try from project root
    if not train_path.exists():
        train_path = project_root / "data/processed/train_threads.csv"
        eval_path = project_root / "data/processed/eval_threads.csv"
    
    if not train_path.exists() or not eval_path.exists():
        print("SKIP: Train/eval split files not found")
        return
    
    train_df = pd.read_csv(train_path)
    eval_df = pd.read_csv(eval_path)
    
    train_conversations = set(train_df['conversation_id'].unique())
    eval_conversations = set(eval_df['conversation_id'].unique())
    
    overlap = train_conversations & eval_conversations
    
    assert len(overlap) == 0, f"Conversation leakage detected: {overlap}"
    print(f"PASS: No conversation leakage. Train: {len(train_conversations)}, Eval: {len(eval_conversations)}")


if __name__ == "__main__":
    test_conversation_leakage()