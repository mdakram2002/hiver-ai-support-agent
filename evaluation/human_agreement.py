import argparse, pandas as pd
from sklearn.metrics import cohen_kappa_score


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--human", required=True)
    p.add_argument("--judge", required=True)
    p.add_argument("--column", default="groundedness")
    a = p.parse_args()
    h = pd.read_csv(a.human)
    j = pd.read_csv(a.judge)
    m = h.merge(j, on="id", suffixes=("_human", "_judge"))
    print(
        {
            "n": len(m),
            "weighted_kappa": cohen_kappa_score(
                m[f"{a.column}_human"], m[f"{a.column}_judge"], weights="quadratic"
            ),
        }
    )


if __name__ == "__main__":
    main()
