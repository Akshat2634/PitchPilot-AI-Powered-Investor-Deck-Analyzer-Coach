'use client'

import React, { useState } from 'react'
import { Upload, FileText, BarChart3, MessageSquare } from 'lucide-react'
import { api } from '@/lib/api'
import { EvaluationResponse, PitchStatus } from '@/types/pitch'

export default function AnalysisDashboard() {
  const [file, setFile] = useState<File | null>(null)
  const [analysis, setAnalysis] = useState<EvaluationResponse | null>(null)
  const [status, setStatus] = useState<PitchStatus>(PitchStatus.PENDING)
  const [isLoading, setIsLoading] = useState(false)

  const handleFileUpload = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!file) return

    setIsLoading(true)
    setStatus(PitchStatus.PROCESSING)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('user_query', 'Provide comprehensive analysis and scoring')

      const result = await api.analyzePitch(formData)
      setAnalysis(result)
      setStatus(PitchStatus.COMPLETED)
    } catch (error) {
      console.error('Analysis failed:', error)
      setStatus(PitchStatus.FAILED)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold mb-8 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          Pitch Analysis Dashboard
        </h1>

        {/* Upload Section */}
        <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700/50 mb-8">
          <form onSubmit={handleFileUpload} className="space-y-6">
            <div className="border-2 border-dashed border-slate-600 rounded-xl p-8 text-center hover:border-blue-500 transition-colors">
              <Upload className="w-12 h-12 text-slate-400 mx-auto mb-4" />
              <input
                type="file"
                accept=".pdf,.pptx,.docx,.txt"
                onChange={(e) => setFile(e.target.files?.[0] || null)}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <span className="text-lg text-slate-300">
                  {file ? file.name : "Drop your pitch deck here or click to browse"}
                </span>
              </label>
            </div>
            
            <button
              type="submit"
              disabled={!file || isLoading}
              className="w-full px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? 'Analyzing...' : 'Start Analysis'}
            </button>
          </form>
        </div>

        {/* Results Section */}
        {analysis && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Feedback */}
            {analysis.feedback && (
              <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700/50">
                <div className="flex items-center mb-6">
                  <MessageSquare className="w-6 h-6 text-blue-400 mr-3" />
                  <h2 className="text-2xl font-bold text-white">Analysis Feedback</h2>
                </div>
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold text-slate-200 mb-2">Overall Feedback</h3>
                    <p className="text-slate-300">{analysis.feedback.overall_feedback}</p>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-green-400 mb-2">Strengths</h3>
                    <p className="text-slate-300">{analysis.feedback.strengths}</p>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-red-400 mb-2">Weaknesses</h3>
                    <p className="text-slate-300">{analysis.feedback.weaknesses}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Scores */}
            {analysis.score && (
              <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700/50">
                <div className="flex items-center mb-6">
                  <BarChart3 className="w-6 h-6 text-purple-400 mr-3" />
                  <h2 className="text-2xl font-bold text-white">Scoring Results</h2>
                </div>
                <div className="space-y-4">
                  {Object.entries(analysis.score).map(([key, value]) => (
                    <div key={key}>
                      <div className="flex justify-between mb-2">
                        <span className="text-slate-300 capitalize">{key}</span>
                        <span className="text-blue-400 font-semibold">{value}/10</span>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-2">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${(value / 10) * 100}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
} 