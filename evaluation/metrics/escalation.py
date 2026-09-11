from sklearn.metrics import precision_recall_fscore_support


def escalation_metrics(expected, predicted):
    p, r, f, _ = precision_recall_fscore_support(
        expected, predicted, average="binary", zero_division=0
    )
    return {"precision": p, "recall": r, "f1": f}
