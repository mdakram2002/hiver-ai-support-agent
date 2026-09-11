import pandas as pd
from pathlib import Path
import sys
import warnings

warnings.filterwarnings("ignore")
sys.path.append(str(Path(__file__).parents[1]))
from metrics.classification import classification_metrics


def predict(train, test):
    # Handle different column names between train and test
    train_intent_col = 'intent' if 'intent' in train.columns else 'expected_intent'
    majority = train[train_intent_col].mode()[0]
    return [majority] * len(test)


if __name__ == "__main__":
    train = pd.read_csv("data/train.csv")
    test = pd.read_csv("golden_set/golden_set.csv")
    print(classification_metrics(test.expected_intent, predict(train, test)))
