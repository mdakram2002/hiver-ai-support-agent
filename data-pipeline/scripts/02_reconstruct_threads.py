import argparse
from pathlib import Path
import pandas as pd


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="../../data/processed/clean.csv")
    p.add_argument("--output", default="../../data/processed/threads.csv")
    a = p.parse_args()
    df = pd.read_csv(a.input, dtype={"tweet_id": "string", "in_response_to_tweet_id": "string"})
    parent = dict(zip(df.tweet_id, df.in_response_to_tweet_id))

    def root(x):
        seen = set()
        while pd.notna(parent.get(x)) and parent[x] not in seen:
            seen.add(x)
            x = parent[x]
        return x

    df["conversation_id"] = df.tweet_id.map(root)
    df["role"] = df.inbound.map(lambda x: "customer" if bool(x) else "agent")
    df["sequence"] = df.groupby("conversation_id").cumcount()
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(a.output, index=False)
    print(f"Wrote {df.conversation_id.nunique()} threads")


if __name__ == "__main__":
    main()
