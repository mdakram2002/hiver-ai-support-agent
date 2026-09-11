"""Profile support-account candidates from the local official CSV by chunks."""

import argparse
import json
from collections import Counter
from pathlib import Path

from dataset_utils import as_bool, read_chunks, validate_columns
import warnings
warnings.filterwarnings("ignore")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("../../data/raw/twcs.csv"))
    parser.add_argument(
        "--output", type=Path, default=Path("../../data/processed/eda_summary.json")
    )
    parser.add_argument("--report", type=Path, default=Path("../../reports/data_eda.md"))
    parser.add_argument("--chunk-size", type=int, default=100_000)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args()
    outbound: Counter[str] = Counter()
    direct_replies: Counter[str] = Counter()
    totals: Counter[str] = Counter()
    for chunk in read_chunks(args.input, args.chunk_size):
        validate_columns(chunk.columns)
        inbound = as_bool(chunk["inbound"])
        totals["rows"] += len(chunk)
        totals["inbound"] += int(inbound.sum())
        totals["outbound"] += int((~inbound).sum())
        for author, count in (
            chunk.loc[~inbound, "author_id"].dropna().astype(str).value_counts().items()
        ):
            outbound[author] += int(count)
        linked = chunk.loc[(~inbound) & chunk["in_response_to_tweet_id"].notna(), "author_id"]
        for author, count in linked.dropna().astype(str).value_counts().items():
            direct_replies[author] += int(count)
    candidates = [
        {"author_id": author, "outbound_messages": count, "direct_replies": direct_replies[author]}
        for author, count in outbound.most_common(args.top)
    ]
    result = {"totals": dict(totals), "top_support_candidates": candidates}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    lines = [
        "# Customer Support on Twitter EDA",
        "",
        "Generated from the locally downloaded official Kaggle CSV.",
        "",
        "## Totals",
        "",
    ]
    lines.extend(f"- {key}: {value}" for key, value in result["totals"].items())
    lines.extend(
        [
            "",
            "## Top outbound support-account candidates",
            "",
            "| author_id | outbound messages | direct replies |",
            "| --- | ---: | ---: |",
        ]
    )
    lines.extend(
        f"| {row['author_id']} | {row['outbound_messages']} | {row['direct_replies']} |"
        for row in candidates
    )
    args.report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
