// Mirror your Python Pydantic models
export interface PitchData {
  pitch_text: string
  user_query?: string
}

export interface FeedbackModel {
  overall_feedback: string
  strengths: string
  weaknesses: string
  opportunities: string
  threats: string
  suggestions: string
}

export interface ScoreModel {
  clarity: number
  differentiation: number
  traction: number
  scalability: number
  overall: number
}

export interface EvaluationResponse {
  pitch?: PitchData
  feedback?: FeedbackModel
  score?: ScoreModel
}

export enum PitchStatus {
  PENDING = "pending",
  PROCESSING = "processing", 
  COMPLETED = "completed",
  FAILED = "failed"
}

export enum FileType {
  PDF = "pdf",
  PPTX = "pptx", 
  DOCX = "docx",
  TXT = "txt"
} 