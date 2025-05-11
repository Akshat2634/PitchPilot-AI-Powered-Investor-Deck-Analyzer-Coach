# app/schemas/pitch.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any, Union
from datetime import datetime
from enum import Enum

class PitchStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class FileType(str, Enum):
    PDF = "pdf"
    PPTX = "pptx"
    DOCX = "docx"
    TXT = "txt"

# Request Models
class PitchCreate(BaseModel):
    title: str
    description: Optional[str] = None
    file_type: Optional[FileType] = None

# Response Models
class PitchResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    file_path: str
    file_type: FileType
    status: PitchStatus
    created_at: datetime
    updated_at: datetime
    
class ScoreItem(BaseModel):
    score: float
    explanation: str
    
class FeedbackResponse(BaseModel):
    id: str
    pitch_id: str
    overall_score: Optional[float] = None
    scores: Optional[Dict[str, ScoreItem]] = None
    suggestions: Optional[Dict[str, List[str]]] = None
    elevator_pitch: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class QuestionItem(BaseModel):
    question: str
    category: str
    importance: str
    rationale: Optional[str] = None
    
class QuestionsResponse(BaseModel):
    id: str
    pitch_id: str
    questions: List[QuestionItem]
    created_at: datetime
    updated_at: datetime

# Combined Responses
class EvaluationResponse(BaseModel):
    pitch: PitchResponse
    feedback: Optional[FeedbackResponse] = None
    questions: Optional[QuestionsResponse] = None