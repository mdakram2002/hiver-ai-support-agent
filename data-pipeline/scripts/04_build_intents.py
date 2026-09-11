"""Export representative messages for human intent-taxonomy review; it does not invent labels."""

import argparse
import json
import warnings
import pandas as pd

warnings.filterwarnings("ignore")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="../../data/processed/threads.csv")
    p.add_argument("--brand", required=True)
    p.add_argument("--output", default="../../data/processed/intent_review.json")
    a = p.parse_args()
    df = pd.read_csv(a.input)
    # Convert inbound to boolean properly
    df['inbound'] = df['inbound'].astype(str).str.lower().isin({'true', '1', 'yes'})
    rows = df[
        (df.inbound == True)
        & (df.conversation_id.isin(df[df.author_id.astype(str) == a.brand].conversation_id))
    ]
    open(a.output, "w", encoding="utf8").write(
        json.dumps(rows[["conversation_id", "text"]].head(300).to_dict("records"), indent=2)
    )
    print("Review exported messages, then write a human-approved taxonomy before classification.")


if __name__ == "__main__":
    main()
