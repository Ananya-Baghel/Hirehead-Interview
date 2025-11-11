from fastapi import FastAPI, UploadFile, File, Body, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
import uuid

from .schemas import *
from .models_core import ensure, train, load
from .logic_adaptive import load_questions, pick_question, analyze_answer, adjust_stress
from .logic_group import PERSONAS
from .logic_culture import culture_fit_score, load_values
from .logic_audio import audio_metrics
from .logic_vision import image_metrics
from .negotiation import start as nego_start, respond as nego_respond

api = FastAPI(title="Interview Bot — Full", version="2.0")
api.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SESSIONS: Dict[str, Dict[str, Any]] = {}
QUESTIONS = load_questions()
ensure()

@api.get("/health")
def health():
    return {"ok": True, "personas": list(PERSONAS.keys())}

@api.post("/train")
def retrain():
    return train()

@api.post("/analyze", response_model=AnalyzeResponse)
def analyze_text(payload: AnalyzeRequest):
    sent, conf = load()
    s = sent.predict([payload.transcript])[0]
    sp = float(sent.predict_proba([payload.transcript])[0].max())
    c = conf.predict([payload.transcript])[0]
    cp = float(conf.predict_proba([payload.transcript])[0].max())
    # simple metrics
    words = payload.transcript.strip().split()
    wpm = None
    if payload.durationSeconds and payload.durationSeconds>0:
        wpm = len(words)/payload.durationSeconds*60.0
    fillers = {}
    for f in ["um","uh","like","you know","actually","basically","literally","sort of","kinda","honestly"]:
        cnt = f" {payload.transcript.lower()} ".count(f" {f} ")
        if cnt>0: fillers[f]=cnt
    tips = []
    if wpm is not None and wpm<90: tips.append("Speed up slightly (~110–140 wpm).")
    if wpm is not None and wpm>160: tips.append("Slow down slightly (~110–140 wpm).")
    if fillers: tips.append("Reduce filler words: "+", ".join([f"{k}×{v}" for k,v in fillers.items()]))
    if s=="neg": tips.append("Keep tone positive; frame learnings and outcomes.")
    if c=="hesitant": tips.append("Use active voice and crisp structure (STAR).")
    if not tips: tips.append("Great delivery. Keep using concrete metrics.")
    next_qs = ["Tell me about a time you led a project under pressure.",
               "Describe a conflict you resolved within a team.",
               "Walk me through a complex problem you solved."]
    return AnalyzeResponse(
        sentiment={"label": s, "confidence": sp},
        confidence={"label": c, "confidence": cp},
        metrics={"word_count": len(words), "wpm": wpm, "fillers": fillers},
        suggestions={"tips": tips, "next_questions": next_qs}
    )

# ---- Interview sessions (adaptive + group) ----
@api.post("/interview/start")
def start_interview(req: StartInterviewRequest):
    sid = str(uuid.uuid4())
    SESSIONS[sid] = {
        "industry": req.industry,
        "personas": [p for p in req.personas if p in PERSONAS] or ["hr"],
        "stress": max(1, min(5, req.stressLevel)),
        "difficulty": req.difficulty,
        "history": []
    }
    persona = SESSIONS[sid]["personas"][0]
    q = pick_question(QUESTIONS, req.industry, persona, req.difficulty, SESSIONS[sid]["stress"])
    return {"sessionId": sid, "persona": persona, "question": q, "stress": SESSIONS[sid]["stress"]}

@api.post("/interview/next")
def next_question(req: NextQuestionRequest):
    s = SESSIONS[req.sessionId]
    sentiment, confidence = ("neutral","confident")
    if req.lastAnswer:
        sentiment, confidence = analyze_answer(req.lastAnswer)
        s["history"].append({"answer": req.lastAnswer, "sentiment": sentiment, "confidence": confidence})
        s["stress"] = adjust_stress(s["stress"], sentiment, confidence)
    # rotate persona
    idx = len(s["history"]) % len(s["personas"])
    persona = s["personas"][idx]
    q = pick_question(QUESTIONS, s["industry"], persona, s["difficulty"], s["stress"])
    return {"persona": persona, "question": q, "stress": s["stress"], "last_eval": {"sentiment": sentiment, "confidence": confidence}}

# ---- Culture fit ----
@api.post("/culturefit/score", response_model=CultureFitResponse)
def culturefit(req: CultureFitRequest):
    values = load_values(req.companyValuesOverride)
    score, keywords = culture_fit_score(req.transcript, values)
    return CultureFitResponse(score=score, top_keywords=keywords)

# ---- Audio analysis (file upload) ----
@api.post("/audio/analyze", response_model=AudioAnalyzeResponse)
async def audio_analyze(file: UploadFile = File(...)):
    data = await file.read()
    m = audio_metrics(data)
    return AudioAnalyzeResponse(**m)

# ---- Image analysis (file upload) ----
@api.post("/image/analyze", response_model=ImageAnalyzeResponse)
async def image_analyze(file: UploadFile = File(...)):
    data = await file.read()
    m = image_metrics(data)
    return ImageAnalyzeResponse(**m)

# ---- Salary negotiation ----
@api.post("/negotiation/start")
def negotiation_start(req: NegotiationStartRequest):
    sid, msg = nego_start(req.role, req.candidateAnchor, req.candidateBATNA)
    return {"sessionId": sid, "message": msg}

@api.post("/negotiation/respond")
def negotiation_respond(req: NegotiationRespondRequest):
    return nego_respond(req.sessionId, req.candidateMessage)

# ---- Real-time WebSocket (live text chunks) ----
@api.websocket("/ws/stream")
async def ws_stream(ws: WebSocket):
    await ws.accept()
    sent, conf = load()
    try:
        # client sends JSON: {"text": "..."} chunks
        while True:
            data = await ws.receive_json()
            text = data.get("text","")
            s = sent.predict([text])[0]; sp = float(sent.predict_proba([text])[0].max())
            c = conf.predict([text])[0]; cp = float(conf.predict_proba([text])[0].max())
            await ws.send_json({"sentiment": {"label": s, "confidence": sp},
                                "confidence": {"label": c, "confidence": cp}})
    except WebSocketDisconnect:
        return
