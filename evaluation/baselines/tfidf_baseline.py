import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from pathlib import Path
import sys
import warnings

warnings.filterwarnings("ignore")
sys.path.append(str(Path(__file__).parents[1]))
from metrics.classification import classification_metrics


def predict(train, test):
    # Handle different column names between train and test
    train_text_col = 'text' if 'text' in train.columns else 'customer_message'
    test_text_col = 'customer_message' if 'customer_message' in test.columns else 'text'
    train_intent_col = 'intent' if 'intent' in train.columns else 'expected_intent'
    
    model = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    x = model.fit_transform(train[train_text_col])
    clf = LogisticRegression(max_iter=1000, class_weight="balanced").fit(x, train[train_intent_col])
    return clf.predict(model.transform(test[test_text_col]))


if __name__ == "__main__":
    train = pd.read_csv("data/train.csv")
    test = pd.read_csv("golden_set/golden_set.csv")
    print(classification_metrics(test.expected_intent, predict(train, test)))
