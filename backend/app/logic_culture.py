from pathlib import Path
from typing import List, Tuple
import json
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

BASE = Path(__file__).resolve().parent.parent
CVAL = BASE / "data" / "company_values.json"

def load_values(values_override: List[str] | None = None) -> List[str]:
    if values_override:
        return values_override
    data = json.loads(CVAL.read_text())
    return data["values_text"]

def culture_fit_score(text: str, values: List[str]) -> Tuple[float, List[str]]:
    corpus = values + [text]
    vec = TfidfVectorizer(stop_words="english")
    X = vec.fit_transform(corpus)
    vals = X[:-1].toarray().mean(axis=0)
    cand = X[-1].toarray()[0]
    score = float(np.dot(vals, cand) / (np.linalg.norm(vals)*np.linalg.norm(cand) + 1e-9))
    # top keywords from candidate aligned with values
    idx = np.argsort(-cand)[:8]
    vocab = np.array([w for w, i in sorted(vec.vocabulary_.items(), key=lambda x:x[1])])
    return score, vocab[idx].tolist()
