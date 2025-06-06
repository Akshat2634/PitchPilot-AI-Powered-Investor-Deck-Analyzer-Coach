'use client'

import React, { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { BarChart3, MessageSquare, ArrowLeft, Download, Share2, CheckCircle, AlertTriangle, TrendingUp } from 'lucide-react'
import { EvaluationResponse } from '@/types/pitch'

export default function AnalysisResults() {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [analysis, setAnalysis] = useState<EvaluationResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const dataParam = searchParams.get('data')
    if (dataParam) {
      try {
        const parsedData = JSON.parse(decodeURIComponent(dataParam))
        setAnalysis(parsedData)
      } catch (error) {
        console.error('Failed to parse analysis data:', error)
      }
    }
    setIsLoading(false)
  }, [searchParams])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-xl text-slate-300">Loading your analysis...</p>
        </div>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-16 h-16 text-yellow-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-2">No Analysis Found</h2>
          <p className="text-slate-400 mb-6">We couldn't find your analysis results.</p>
          <button 
            onClick={() => router.push('/upload')}
            className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-200"
          >
            Start New Analysis
          </button>
        </div>
      </div>
    )
  }

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-400'
    if (score >= 6) return 'text-yellow-400'
    return 'text-red-400'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 8) return 'Excellent'
    if (score >= 6) return 'Good'
    if (score >= 4) return 'Fair'
    return 'Needs Improvement'
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <div className="border-b border-slate-800/50">
        <div className="max-w-7xl mx-auto px-6 py-6">
          <button 
            onClick={() => router.back()}
            className="flex items-center text-slate-400 hover:text-white transition-colors duration-200 mb-6"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Upload
          </button>
          
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            <div>
              <h1 className="text-4xl lg:text-5xl font-bold mb-4 text-white">
                Pitch Analysis Results
              </h1>
              <p className="text-xl text-slate-400">
                AI-powered insights and recommendations for your pitch
              </p>
            </div>
            
            <div className="flex items-center gap-4 mt-6 lg:mt-0">
              <button className="flex items-center px-4 py-2 bg-slate-800/50 border border-slate-700/50 rounded-xl hover:bg-slate-700/50 transition-all duration-200">
                <Download className="w-5 h-5 mr-2" />
                Export PDF
              </button>
              <button className="flex items-center px-4 py-2 bg-slate-800/50 border border-slate-700/50 rounded-xl hover:bg-slate-700/50 transition-all duration-200">
                <Share2 className="w-5 h-5 mr-2" />
                Share
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-12">
        {/* Overall Score */}
        {analysis.score && (
          <div className="bg-slate-900/50 rounded-2xl border border-slate-800/50 p-8 mb-8">
            <div className="text-center">
              <div className="inline-flex items-center justify-center w-32 h-32 rounded-full bg-gradient-to-br from-blue-500/20 to-purple-600/20 border border-blue-500/30 mb-6">
                <div className="text-center">
                  <div className={`text-4xl font-bold ${getScoreColor(analysis.score.overall)}`}>
                    {analysis.score.overall}/10
                  </div>
                  <div className="text-sm text-slate-400 mt-1">Overall Score</div>
                </div>
              </div>
              <h2 className="text-2xl font-bold text-white mb-2">
                {getScoreLabel(analysis.score.overall)} Pitch
              </h2>
              <p className="text-slate-400">
                Your pitch has been analyzed across multiple dimensions
              </p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Detailed Scores */}
          {analysis.score && (
            <div className="bg-slate-900/50 rounded-2xl border border-slate-800/50 p-8">
              <div className="flex items-center mb-6">
                <BarChart3 className="w-6 h-6 text-purple-400 mr-3" />
                <h2 className="text-2xl font-bold text-white">Detailed Scoring</h2>
              </div>
              
              <div className="space-y-6">
                {Object.entries(analysis.score).map(([key, value]) => {
                  if (key === 'overall') return null
                  return (
                    <div key={key}>
                      <div className="flex justify-between items-center mb-3">
                        <span className="text-lg font-medium text-slate-200 capitalize">
                          {key.replace('_', ' ')}
                        </span>
                        <div className="text-right">
                          <span className={`text-xl font-bold ${getScoreColor(value)}`}>
                            {value}/10
                          </span>
                          <div className="text-sm text-slate-400">
                            {getScoreLabel(value)}
                          </div>
                        </div>
                      </div>
                      <div className="w-full bg-slate-700 rounded-full h-3">
                        <div 
                          className={`h-3 rounded-full transition-all duration-1000 ${
                            value >= 8 ? 'bg-gradient-to-r from-green-500 to-green-400' :
                            value >= 6 ? 'bg-gradient-to-r from-yellow-500 to-yellow-400' :
                            'bg-gradient-to-r from-red-500 to-red-400'
                          }`}
                          style={{ width: `${(value / 10) * 100}%` }}
                        />
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          )}

          {/* Key Insights */}
          <div className="bg-slate-900/50 rounded-2xl border border-slate-800/50 p-8">
            <div className="flex items-center mb-6">
              <TrendingUp className="w-6 h-6 text-blue-400 mr-3" />
              <h2 className="text-2xl font-bold text-white">Key Insights</h2>
            </div>
            
            <div className="space-y-4">
              <div className="p-4 bg-green-500/10 rounded-xl border border-green-500/20">
                <div className="flex items-center mb-2">
                  <CheckCircle className="w-5 h-5 text-green-400 mr-2" />
                  <span className="text-green-300 font-semibold">Top Strength</span>
                </div>
                <p className="text-slate-300 text-sm">
                  {analysis.feedback?.strengths.split('.')[0]}...
                </p>
              </div>
              
              <div className="p-4 bg-yellow-500/10 rounded-xl border border-yellow-500/20">
                <div className="flex items-center mb-2">
                  <AlertTriangle className="w-5 h-5 text-yellow-400 mr-2" />
                  <span className="text-yellow-300 font-semibold">Priority Area</span>
                </div>
                <p className="text-slate-300 text-sm">
                  {analysis.feedback?.weaknesses.split('.')[0]}...
                </p>
              </div>
              
              <div className="p-4 bg-blue-500/10 rounded-xl border border-blue-500/20">
                <div className="flex items-center mb-2">
                  <TrendingUp className="w-5 h-5 text-blue-400 mr-2" />
                  <span className="text-blue-300 font-semibold">Growth Opportunity</span>
                </div>
                <p className="text-slate-300 text-sm">
                  {analysis.feedback?.opportunities.split('.')[0]}...
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Detailed Feedback */}
        {analysis.feedback && (
          <div className="mt-8 bg-slate-900/50 rounded-2xl border border-slate-800/50 p-8">
            <div className="flex items-center mb-8">
              <MessageSquare className="w-6 h-6 text-blue-400 mr-3" />
              <h2 className="text-2xl font-bold text-white">Detailed Analysis</h2>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold text-slate-200 mb-3 flex items-center">
                    <CheckCircle className="w-5 h-5 text-green-400 mr-2" />
                    Strengths
                  </h3>
                  <div className="p-4 bg-green-500/5 rounded-xl border border-green-500/20">
                    <p className="text-slate-300 leading-relaxed">{analysis.feedback.strengths}</p>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-slate-200 mb-3 flex items-center">
                    <TrendingUp className="w-5 h-5 text-blue-400 mr-2" />
                    Opportunities
                  </h3>
                  <div className="p-4 bg-blue-500/5 rounded-xl border border-blue-500/20">
                    <p className="text-slate-300 leading-relaxed">{analysis.feedback.opportunities}</p>
                  </div>
                </div>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold text-slate-200 mb-3 flex items-center">
                    <AlertTriangle className="w-5 h-5 text-yellow-400 mr-2" />
                    Areas for Improvement
                  </h3>
                  <div className="p-4 bg-yellow-500/5 rounded-xl border border-yellow-500/20">
                    <p className="text-slate-300 leading-relaxed">{analysis.feedback.weaknesses}</p>
                  </div>
                </div>

                <div>
                  <h3 className="text-xl font-semibold text-slate-200 mb-3 flex items-center">
                    <MessageSquare className="w-5 h-5 text-purple-400 mr-2" />
                    Recommendations
                  </h3>
                  <div className="p-4 bg-purple-500/5 rounded-xl border border-purple-500/20">
                    <p className="text-slate-300 leading-relaxed">{analysis.feedback.suggestions}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Overall Feedback */}
            <div className="mt-8 p-6 bg-slate-800/30 rounded-xl border border-slate-700/30">
              <h3 className="text-xl font-semibold text-slate-200 mb-4">Overall Assessment</h3>
              <p className="text-slate-300 leading-relaxed text-lg">{analysis.feedback.overall_feedback}</p>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="mt-12 flex flex-col sm:flex-row items-center justify-center gap-6">
          <button 
            onClick={() => router.push('/upload')}
            className="px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-200 text-lg font-semibold"
          >
            Analyze Another Pitch
          </button>
          <button className="px-8 py-4 bg-slate-800/50 border border-slate-700/50 rounded-xl hover:bg-slate-700/50 transition-all duration-200 text-lg font-semibold">
            Schedule Expert Review
          </button>
        </div>
      </div>
    </div>
  )
} 