"""Load reviewed, embedded historical resolutions into pgvector."""

import argparse
import json
import os
import warnings
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
import psycopg

warnings.filterwarnings("ignore")
load_dotenv(Path(__file__).resolve().parents[2] / ".env")


REQUIRED_COLUMNS = {
    "conversation_id",
    "brand",
    "customer_message",
    "agent_response",
    "intent",
    "embedding",
}


def parse_embedding(value: object) -> list[float]:
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, list) or len(value) != 1536:
        raise ValueError("Each embedding must be a 1536-dimension JSON array.")
    return [float(item) for item in value]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="../../data/processed/resolution_pairs_embedded.csv")
    parser.add_argument("--database-url", default=os.getenv("DATABASE_URL"))
    parser.add_argument(
        "--replace-brand",
        action="store_true",
        help="Delete existing examples for this brand before import.",
    )
    args = parser.parse_args()

    if not args.database_url:
        raise RuntimeError("Set DATABASE_URL or pass --database-url.")

    pairs = pd.read_csv(args.input)
    missing = REQUIRED_COLUMNS - set(pairs.columns)
    if missing:
        raise ValueError(f"Input is missing required columns: {sorted(missing)}")
    if pairs.empty:
        raise ValueError("No embedded resolution pairs are available to import.")
    if pairs.intent.isna().any() or pairs.intent.astype(str).str.strip().eq("UNLABELLED").any():
        raise ValueError("UNLABELLED pairs must not be imported.")

    brands = pairs.brand.dropna().astype(str).unique()
    if len(brands) != 1:
        raise ValueError("The import file must contain exactly one brand.")

    with psycopg.connect(args.database_url) as connection, connection.cursor() as cursor:
        if args.replace_brand:
            cursor.execute("DELETE FROM resolution_examples WHERE brand = %s", (brands[0],))
        for row in pairs.itertuples(index=False):
            embedding = parse_embedding(row.embedding)
            cursor.execute(
                """
                INSERT INTO resolution_examples
                  (conversation_id, brand, customer_message, agent_response, intent, embedding)
                VALUES (%s, %s, %s, %s, %s, %s::vector)
                """,
                (
                    str(row.conversation_id),
                    str(row.brand),
                    str(row.customer_message),
                    str(row.agent_response),
                    str(row.intent),
                    json.dumps(embedding),
                ),
            )
    print(f"Imported {len(pairs)} reviewed resolution pairs for brand {brands[0]}.")


if __name__ == "__main__":
    main()
