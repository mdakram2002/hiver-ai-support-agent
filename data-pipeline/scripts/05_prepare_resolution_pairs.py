import argparse
import warnings
from pathlib import Path
import pandas as pd

warnings.filterwarnings("ignore")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="../../data/processed/train_threads.csv")
    p.add_argument("--brand", required=True)
    p.add_argument("--output", default="../../data/processed/resolution_pairs.csv")
    a = p.parse_args()
    df = pd.read_csv(a.input)
    # Filter for brand conversations only
    brand_conversations = df[df.author_id.astype(str) == a.brand].conversation_id.unique()
    df = df[df.conversation_id.isin(brand_conversations)].sort_values(["conversation_id", "sequence"])
    pairs = []
    for cid, g in df.groupby("conversation_id"):
        g = g.reset_index(drop=True)
        for i, row in g.iterrows():
            if row.role == "customer" and i + 1 < len(g) and g.loc[i + 1, "role"] == "agent":
                pairs.append(
                    {
                        "conversation_id": cid,
                        "customer_message": row.text,
                        "agent_response": g.loc[i + 1, "text"],
                        "intent": "UNLABELLED",
                    }
                )
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(pairs).to_csv(a.output, index=False)
    print(
        f"Wrote {len(pairs)} candidate pairs. Human review and intent labels are required before indexing."
    )


if __name__ == "__main__":
    main()
