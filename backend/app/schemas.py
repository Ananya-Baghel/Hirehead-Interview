from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class AnalyzeRequest(BaseModel):
    transcript: str
    durationSeconds: Optional[float] = None

class AnalyzeResponse(BaseModel):
    sentiment: Dict[str, Any]
    confidence: Dict[str, Any]
    metrics: Dict[str, Any]
    suggestions: Dict[str, Any]

class StartInterviewRequest(BaseModel):
    industry: str = Field(..., description="e.g., software, marketing, finance")
    personas: List[str] = Field(..., description="e.g., ['hr','tech','manager']")
    difficulty: str = Field("easy", description="easy|medium|hard")
    stressLevel: int = Field(1, description="1..5")

class NextQuestionRequest(BaseModel):
    sessionId: str
    lastAnswer: Optional[str] = None
    durationSeconds: Optional[float] = None

class CultureFitRequest(BaseModel):
    transcript: str
    companyValuesOverride: Optional[List[str]] = None

class CultureFitResponse(BaseModel):
    score: float
    top_keywords: List[str]

class NegotiationStartRequest(BaseModel):
    role: str
    candidateAnchor: float = Field(..., description="candidate expected CTC/LPA")
    candidateBATNA: Optional[str] = None

class NegotiationRespondRequest(BaseModel):
    sessionId: str
    candidateMessage: str

class AudioAnalyzeResponse(BaseModel):
    duration_s: float
    est_syllables_per_sec: float
    est_wpm: float
    mean_amplitude: float
    pitch_hz: Optional[float] = None

class ImageAnalyzeResponse(BaseModel):
    face_detected: bool
    eyes_ratio: Optional[float] = None
    head_tilt_deg: Optional[float] = None
    posture: str
