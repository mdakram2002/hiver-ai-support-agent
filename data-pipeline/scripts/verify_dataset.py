"""Validate the official dataset schema and calculate summary statistics by chunks."""

import argparse
import json
import sqlite3
import warnings
from collections import Counter
from pathlib import Path

import pandas as pd

from dataset_utils import as_bool, read_chunks, validate_columns

warnings.filterwarnings("ignore")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("../../data/raw/twcs.csv"))
    parser.add_argument(
        "--output", type=Path, default=Path("../../data/processed/dataset_verification.json")
    )
    parser.add_argument("--chunk-size", type=int, default=100_000)
    args = parser.parse_args()
    if not args.input.exists():
        raise FileNotFoundError(f"Dataset not found: {args.input}")
    totals: Counter[str] = Counter()
    nulls: Counter[str] = Counter()
    date_min = date_max = None
    temporary_db = args.output.with_suffix(".sqlite")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(temporary_db) as database:
        database.execute("DROP TABLE IF EXISTS unique_ids")
        database.execute("DROP TABLE IF EXISTS unique_authors")
        database.execute("CREATE TABLE unique_ids (tweet_id TEXT PRIMARY KEY)")
        database.execute("CREATE TABLE unique_authors (author_id TEXT PRIMARY KEY)")
        for chunk in read_chunks(args.input, args.chunk_size):
            validate_columns(chunk.columns)
            inbound = as_bool(chunk["inbound"])
            totals["rows"] += len(chunk)
            totals["inbound"] += int(inbound.sum())
            totals["outbound"] += int((~inbound).sum())
            totals["response_links"] += int(chunk["response_tweet_id"].notna().sum())
            nulls.update({column: int(chunk[column].isna().sum()) for column in chunk.columns})
            dates = pd.to_datetime(chunk["created_at"], errors="coerce", utc=True).dropna()
            if not dates.empty:
                date_min = dates.min() if date_min is None else min(date_min, dates.min())
                date_max = dates.max() if date_max is None else max(date_max, dates.max())
            database.executemany(
                "INSERT OR IGNORE INTO unique_ids VALUES (?)",
                ((str(value),) for value in chunk["tweet_id"].dropna().unique()),
            )
            database.executemany(
                "INSERT OR IGNORE INTO unique_authors VALUES (?)",
                ((str(value),) for value in chunk["author_id"].dropna().unique()),
            )
        totals["unique_tweet_ids"] = database.execute("SELECT COUNT(*) FROM unique_ids").fetchone()[
            0
        ]
        totals["unique_author_ids"] = database.execute(
            "SELECT COUNT(*) FROM unique_authors"
        ).fetchone()[0]
    # Clean up SQLite database
    try:
        temporary_db.unlink(missing_ok=True)
    except PermissionError:
        # On Windows, the file might be locked temporarily
        pass
    result = {
        "input": str(args.input),
        **totals,
        "null_counts": dict(nulls),
        "date_range": {
            "start": date_min.isoformat() if date_min is not None else None,
            "end": date_max.isoformat() if date_max is not None else None,
        },
    }
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
