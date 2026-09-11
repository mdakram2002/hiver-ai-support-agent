import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parents[2] / "evaluation"))
from metrics.classification import classification_metrics
from metrics.retrieval import retrieval_metrics


def test_classification_metrics():
    assert classification_metrics(["a", "b"], ["a", "a"])["accuracy"] == 0.5


def test_retrieval_metrics():
    assert retrieval_metrics([["x", "y"]], [{"y"}], 2)["hit_at_2"] == 1
