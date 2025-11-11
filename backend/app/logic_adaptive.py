import pandas as pd
from pathlib import Path
from typing import List, Dict
from .logic_group import Persona
from .models_core import load

BASE = Path(__file__).resolve().parent.parent
QPATH = BASE / "data" / "question_bank.csv"

def load_questions():
    df = pd.read_csv(QPATH)
    return df

def pick_question(df, industry: str, persona: str, difficulty: str, stress: int) -> str:
    # increase difficulty with stress
    diffs = ["easy", "medium", "hard"]
    idx = max(0, min(diffs.index(difficulty) + (stress-1)//2, 2))
    target = diffs[idx]
    subset = df[(df["industry"]==industry) & (df["persona"]==persona) & (df["difficulty"]==target)]
    if subset.empty:
        subset = df[(df["industry"]==industry)]
    if subset.empty:
        subset = df
    return subset.sample(1, random_state=None)["question"].iloc[0]

def analyze_answer(answer: str):
    sent, conf = load()
    s = sent.predict([answer])[0]
    c = conf.predict([answer])[0]
    return s, c

def adjust_stress(current_stress: int, sentiment: str, confidence: str) -> int:
    # negative or hesitant -> +1 stress, positive+confident -> -1, clamp 1..5
    delta = 0
    if sentiment == "neg" or confidence == "hesitant":
        delta = 1
    elif sentiment == "pos" and confidence == "confident":
        delta = -1
    lvl = max(1, min(5, current_stress + delta))
    return lvl
