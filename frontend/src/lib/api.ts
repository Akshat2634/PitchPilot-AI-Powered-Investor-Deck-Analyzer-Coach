import { EvaluationResponse } from '@/types/pitch'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export class PitchPilotAPI {
  private baseURL: string

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL
  }

  // Upload and analyze pitch
  async analyzePitch(formData: FormData): Promise<EvaluationResponse> {
    const response = await fetch(`${this.baseURL}/api/analyze`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  // Get analysis by ID
  async getAnalysis(analysisId: string): Promise<EvaluationResponse> {
    const response = await fetch(`${this.baseURL}/api/analysis/${analysisId}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    return response.json()
  }

  // Health check
  async healthCheck(): Promise<{ status: string }> {
    const response = await fetch(`${this.baseURL}/health`)
    return response.json()
  }
}

export const api = new PitchPilotAPI() 