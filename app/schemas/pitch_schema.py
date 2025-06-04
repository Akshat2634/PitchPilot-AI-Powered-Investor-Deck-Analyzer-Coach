# app/schemas/pitch.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any, Union, Literal
from datetime import datetime
from enum import Enum
from typing_extensions import TypedDict
from langgraph.graph import MessagesState

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
    
    
class PitchAction(str, Enum):
    ANALYSIS = "analysis"
    SCORING = "scoring"
    ALL = "all"


# Request Models
class PitchCreate(BaseModel):
    title: str
    description: Optional[str] = None
    file_type: Optional[FileType] = None
    file_content: Optional[str] = None

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

    
class FeedbackModel(BaseModel):
    """
    Pydantic model for feedback data.
    """
    overall_feedback: str = Field(default="", description="Overall feedback on the pitch")
    strengths: str = Field(default="", description="Strengths of the pitch")
    weaknesses: str = Field(default="", description="Weaknesses of the pitch")
    opportunities: str = Field(default="", description="Opportunities for the pitch")
    threats: str = Field(default="", description="Threats to the pitch")
    suggestions: str = Field(default="", description="Suggestions for improvement")
    
class ScoreModel(BaseModel):
    """
    Pydantic model for score data.
    """
    clarity: float = Field(default=0.0, description="Score for clarity of the pitch")
    differentiation: float = Field(default=0.0, description="Score for differentiation from competitors")
    traction: float = Field(default=0.0, description="Score for demonstrated traction")
    scalability: float = Field(default=0.0, description="Score for scalability potential")
    overall: float = Field(default=0.0, description="Overall score of the pitch")
    
class PitchData(BaseModel):
    """
    Pydantic model for pitch data.
    """
    pitch_text: str = Field(default="", description="Extracted text of the the elevator pitch")
    user_query: Optional[str] = Field(default=None, description="User's specific query or request for the pitch analysis")
    # action: Literal["analysis", "scoring", "complete"] = Field(..., description="Requested action: analysis, scoring, or complete")
    
class NextAgentResponse(BaseModel):
    agent_name: str = Field(default="", description="The name of the next agent to call (pitch_analysis_agent or score_pitch_agent)")

class WorkflowClassifier(BaseModel):
    """
    Pydantic model for workflow classification.
    """
    workflow_stage: Literal["analysis", "scoring", "complete"] = Field(
        ...,
        description="Classify the current workflow stage: 'analysis' if feedback is needed, 'scoring' if score is needed, 'complete' if the workflow is complete"
    )


class EvaluationResponse(BaseModel):
    pitch: Optional[PitchData] = None
    feedback: Optional[FeedbackModel] = None
    score: Optional[ScoreModel] = None
    
    
class State(MessagesState):
    """
    Type definition for the state of the application.
    """
    pitch_data: Optional[PitchData] = None
    feedback: Optional[FeedbackModel] = None
    score: Optional[ScoreModel] = None
    workflow_stage: Optional[str] = None
    next_step: Optional[str] = None
    user_query: Optional[str] = None
