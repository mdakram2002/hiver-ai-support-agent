import argparse
import os
import random
import warnings
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

warnings.filterwarnings("ignore")
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="../../data/processed/resolution_pairs_labeled.csv")
    p.add_argument("--output", default="../../data/processed/resolution_pairs_embedded.csv")
    p.add_argument("--brand", required=True)
    a = p.parse_args()
    df = pd.read_csv(a.input)
    required = {"conversation_id", "customer_message", "agent_response", "intent"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Input is missing required columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("No resolution pairs are available to embed.")
    if df.intent.isna().any() or df.intent.astype(str).str.strip().eq("UNLABELLED").any():
        raise ValueError("Review every pair and replace UNLABELLED intents before embedding.")
    df["brand"] = a.brand
    if "OPENAI_API_KEY" not in os.environ or not os.environ["OPENAI_API_KEY"]:
        print("Warning: OPENAI_API_KEY not set. Using dummy embeddings for demonstration.")
        # Create dummy embeddings (1536 dimensions)
        random.seed(42)  # For reproducibility
        df["embedding"] = df.customer_message.map(
            lambda x: [random.random() for _ in range(1536)]
        )
    else:
        c = OpenAI()
        print(f"Generating embeddings for {len(df)} resolution pairs...")
        df["embedding"] = df.customer_message.map(
            lambda x: c.embeddings.create(model="text-embedding-3-small", input=x).data[0].embedding
        )
    df.to_csv(a.output, index=False)
    print(f"Saved embedded pairs to {a.output}")


if __name__ == "__main__":
    main()
