from pathlib import Path
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "interview_training.csv"
MODELS = BASE / "models"
MODELS.mkdir(parents=True, exist_ok=True)

SENT_PATH = MODELS / "sentiment.joblib"
CONF_PATH = MODELS / "confidence.joblib"

def train():
    df = pd.read_csv(DATA)
    df["text"] = df["text"].fillna("")

    # Sentiment
    Xs, ys = df["text"], df["sentiment_label"]
    Xtr, Xte, ytr, yte = train_test_split(Xs, ys, test_size=0.2, random_state=42, stratify=ys)
    sent = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1,2))), ("clf", LogisticRegression(max_iter=1000))])
    sent.fit(Xtr, ytr)
    joblib.dump(sent, SENT_PATH)
    srep = classification_report(yte, sent.predict(Xte), output_dict=True)

    # Confidence
    yc = df["confidence_label"]
    Xtr, Xte, ytr, yte = train_test_split(Xs, yc, test_size=0.2, random_state=42, stratify=yc)
    conf = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1,2))), ("clf", LogisticRegression(max_iter=1000))])
    conf.fit(Xtr, ytr)
    joblib.dump(conf, CONF_PATH)
    crep = classification_report(yte, conf.predict(Xte), output_dict=True)

    return {"sentiment_report": srep, "confidence_report": crep}

def ensure():
    if not SENT_PATH.exists() or not CONF_PATH.exists():
        return train()
    return {"ok": True}

def load():
    import joblib
    return joblib.load(SENT_PATH), joblib.load(CONF_PATH)
