"""Mock import script for demonstration when PostgreSQL is not available."""

import argparse
import json
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="../../data/processed/resolution_pairs_embedded.csv")
    parser.add_argument("--output", default="../../data/processed/import_metadata.json")
    args = parser.parse_args()
    
    # Load embedded pairs
    df = pd.read_csv(args.input)
    print(f"Loaded {len(df)} embedded resolution pairs")
    
    # Validate required columns
    required_columns = {"conversation_id", "brand", "customer_message", "agent_response", "intent", "embedding"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Input is missing required columns: {sorted(missing)}")
    
    # Check brand consistency
    brands = df.brand.dropna().astype(str).unique()
    if len(brands) != 1:
        raise ValueError(f"The import file must contain exactly one brand, found: {brands}")
    
    # Validate embeddings
    print("Validating embeddings...")
    for idx, row in df.iterrows():
        try:
            embedding = json.loads(row.embedding) if isinstance(row.embedding, str) else row.embedding
            if not isinstance(embedding, list) or len(embedding) != 1536:
                raise ValueError(f"Row {idx}: Invalid embedding dimensions")
        except Exception as e:
            raise ValueError(f"Row {idx}: Invalid embedding format - {e}")
    
    print("All embeddings validated successfully")
    
    # Create import metadata (simulating successful import)
    intent_dist = df['intent'].value_counts()
    metadata = {
        "import_status": "MOCK_IMPORT_SUCCESS",
        "brand": brands[0],
        "total_pairs_imported": len(df),
        "intent_distribution": {str(k): int(v) for k, v in intent_dist.items()},
        "note": "This is a mock import. PostgreSQL database not available.",
        "embeddings_validated": True,
        "timestamp": "2026-09-11"
    }
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Mock import completed for {len(df)} pairs")
    print(f"Brand: {brands[0]}")
    print(f"Saved import metadata to {args.output}")
    print("Note: This is a demonstration. In production, data would be imported to PostgreSQL with pgvector.")


if __name__ == "__main__":
    main()