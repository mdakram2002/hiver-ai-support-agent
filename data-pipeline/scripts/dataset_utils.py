"""Shared, streaming-safe helpers for the Twitter support dataset."""

from collections.abc import Iterator
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "tweet_id",
    "author_id",
    "inbound",
    "created_at",
    "text",
    "response_tweet_id",
    "in_response_to_tweet_id",
}


def read_chunks(path: Path, chunk_size: int) -> Iterator[pd.DataFrame]:
    yield from pd.read_csv(
        path, chunksize=chunk_size, dtype={"tweet_id": "string", "author_id": "string"}
    )


def validate_columns(columns: object) -> None:
    missing = REQUIRED_COLUMNS - set(columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")


def as_bool(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().str.lower().isin({"true", "1", "yes"})
