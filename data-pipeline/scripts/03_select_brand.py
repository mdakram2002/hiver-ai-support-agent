import argparse
import pandas as pd


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="../../data/processed/threads.csv")
    p.add_argument("--brand", required=True)
    a = p.parse_args()
    df = pd.read_csv(a.input)
    brand = df[df.author_id.astype(str).eq(a.brand)]
    if brand.empty:
        raise ValueError("Brand author_id is absent; inspect author_id values before selecting.")
    print(
        {
            "brand": a.brand,
            "agent_messages": len(brand),
            "threads": brand.conversation_id.nunique(),
            "avg_thread_length": round(
                df[df.conversation_id.isin(brand.conversation_id)]
                .groupby("conversation_id")
                .size()
                .mean(),
                2,
            ),
        }
    )


if __name__ == "__main__":
    main()
