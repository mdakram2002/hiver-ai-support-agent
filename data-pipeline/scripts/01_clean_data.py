"""Clean a CSV subsample of Kaggle's Customer Support on Twitter data."""

import argparse
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")


def text(value):
    return " ".join(str(value or "").split())


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--output", default="../../data/processed/clean.csv")
    p.add_argument("--sample-size", type=int, default=50000)
    a = p.parse_args()
    df = pd.read_csv(a.input, nrows=a.sample_size)
    required = {"tweet_id", "author_id", "text", "in_response_to_tweet_id", "inbound"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Unexpected CSV columns; missing {sorted(missing)}")
    df["text"] = df.text.map(text)
    df = df[df.text.str.len().between(2, 2000)].drop_duplicates(subset=["tweet_id"])
    if "created_at" in df:
        df["created_at"] = pd.to_datetime(df.created_at, errors="coerce", utc=True)
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.output, index=False)
    print(f"Wrote {len(df)} cleaned messages to {a.output}")


if __name__ == "__main__":
    main()
