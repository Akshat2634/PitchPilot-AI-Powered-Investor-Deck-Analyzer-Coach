'use client'

import React, { useState, useRef, useEffect } from 'react'
import { Upload, FileText, ArrowLeft } from 'lucide-react'
import { useRouter } from 'next/navigation'
import { api } from '@/lib/api'

// Custom hook for typing effect
const useTypingEffect = (text: string, speed: number = 100, delay: number = 0) => {
  const [displayText, setDisplayText] = useState('')
  
  useEffect(() => {
    const timer = setTimeout(() => {
      let i = 0
      const typingInterval = setInterval(() => {
        if (i < text.length) {
          setDisplayText(text.slice(0, i + 1))
          i++
        } else {
          clearInterval(typingInterval)
        }
      }, speed)
      
      return () => clearInterval(typingInterval)
    }, delay)
    
    return () => clearTimeout(timer)
  }, [text, speed, delay])
  
  return displayText
}

export default function UploadPitchForm() {
  const router = useRouter()
  const fileInputRef = useRef<HTMLInputElement>(null)
  
  const [file, setFile] = useState<File | null>(null)
  const [pitchTitle, setPitchTitle] = useState('')
  const [description, setDescription] = useState('')
  const [analysisFocus, setAnalysisFocus] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [dragActive, setDragActive] = useState(false)
  const [isVisible, setIsVisible] = useState(false)

  // Typing effect placeholders
  const titlePlaceholder = useTypingEffect('Enter your pitch title', 80, 1000)
  const descriptionPlaceholder = useTypingEffect('Brief description about your startup', 60, 1500)
  const focusPlaceholder = useTypingEffect('Describe what you want me to analyze, score, or evaluate in your pitch. Be specific about your goals and areas of focus.', 50, 2000)

  useEffect(() => {
    // Trigger animation after component mounts
    const timer = setTimeout(() => {
      setIsVisible(true)
    }, 100)
    return () => clearTimeout(timer)
  }, [])

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
    }
  }

  const handleBrowseClick = () => {
    fileInputRef.current?.click()
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file || !pitchTitle.trim() || !analysisFocus.trim()) return

    setIsLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('pitch_title', pitchTitle.trim())
      formData.append('description', description.trim())
      formData.append('user_query', analysisFocus.trim())

      const result = await api.analyzePitch(formData)
      
      // Navigate to results page with the analysis data
      router.push(`/results?data=${encodeURIComponent(JSON.stringify(result))}`)
    } catch (error) {
      console.error('Analysis failed:', error)
      alert('Analysis failed. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const isValidFileType = (file: File) => {
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
    return validTypes.includes(file.type)
  }

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <div className={`border-b border-slate-800/50 transition-all duration-700 ease-out ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'
      }`}>
        <div className="max-w-4xl mx-auto px-6 py-6">
          <button 
            onClick={() => router.push('/')}
            className="flex items-center text-slate-400 hover:text-white transition-colors duration-200 mb-6"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back
          </button>
          
          <div className="text-center">
            <h1 className="text-4xl lg:text-5xl font-bold mb-4 text-white">
              Upload Your Pitch Deck
            </h1>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto">
              Get AI-powered analysis and feedback on your investor presentation
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className={`max-w-4xl mx-auto px-6 py-12 transition-all duration-700 ease-out delay-200 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
      }`}>
        <div className="bg-slate-900/50 rounded-2xl border border-slate-800/50 p-8">
          <div className="flex items-center mb-8">
            <Upload className="w-6 h-6 text-blue-400 mr-3" />
            <h2 className="text-2xl font-bold text-white">Upload Pitch Document</h2>
          </div>

          <form onSubmit={handleSubmit} className="space-y-8">
            {/* File Upload */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-3">
                Pitch Document <span className="text-red-400">*</span>
              </label>
              
              <div
                className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 ${
                  dragActive 
                    ? 'border-blue-500 bg-blue-500/10' 
                    : file 
                      ? 'border-green-500 bg-green-500/10'
                      : 'border-slate-600 hover:border-slate-500'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.pptx,.docx,.txt"
                  onChange={handleFileChange}
                  className="hidden"
                />
                
                {file ? (
                  <div className="space-y-3">
                    <FileText className="w-12 h-12 text-green-400 mx-auto" />
                    <div>
                      <p className="text-lg font-medium text-white">{file.name}</p>
                      <p className="text-sm text-slate-400">{formatFileSize(file.size)}</p>
                    </div>
                    <button
                      type="button"
                      onClick={() => setFile(null)}
                      className="text-red-400 hover:text-red-300 text-sm underline"
                    >
                      Remove file
                    </button>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <Upload className="w-12 h-12 text-slate-400 mx-auto" />
                    <div>
                      <p className="text-lg text-slate-300 mb-2">
                        Drop your file here, or{' '}
                        <button
                          type="button"
                          onClick={handleBrowseClick}
                          className="text-blue-400 hover:text-blue-300 underline"
                        >
                          browse
                        </button>
                      </p>
                      <p className="text-sm text-slate-500">
                        Supports PDF, PPTX, DOCX, TXT (max 10MB)
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Pitch Title */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-3">
                Pitch Title <span className="text-red-400">*</span>
              </label>
              <input
                type="text"
                value={pitchTitle}
                onChange={(e) => setPitchTitle(e.target.value)}
                placeholder={titlePlaceholder}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200"
                required
              />
            </div>

            {/* Description */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-3">
                Description (Optional)
              </label>
              <textarea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder={descriptionPlaceholder}
                rows={4}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200 resize-none"
              />
            </div>

            {/* Analysis Prompt */}
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-3">
                AI Analysis Prompt <span className="text-red-400">*</span>
              </label>
              <textarea
                value={analysisFocus}
                onChange={(e) => setAnalysisFocus(e.target.value)}
                placeholder={focusPlaceholder}
                rows={4}
                className="w-full px-4 py-3 bg-slate-800/50 border border-slate-700/50 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500/50 transition-all duration-200 resize-none"
                required
              />
              <p className="text-xs text-slate-500 mt-2">
                Tell our AI what specific aspects to analyze, score, or evaluate. Examples: &ldquo;Focus on market opportunity and competitive analysis&rdquo; or &ldquo;Evaluate the financial projections and funding ask&rdquo;
              </p>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={!file || !pitchTitle.trim() || !analysisFocus.trim() || isLoading}
              className="w-full px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed text-lg font-semibold flex items-center justify-center"
            >
              {isLoading ? (
                <div className="flex items-center">
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin mr-3"></div>
                  Analyzing Pitch...
                </div>
              ) : (
                <div className="flex items-center">
                  <FileText className="w-5 h-5 mr-2" />
                  Analyze Pitch
                </div>
              )}
            </button>

            {/* File validation message */}
            {file && !isValidFileType(file) && (
              <div className="text-red-400 text-sm text-center">
                Please upload a valid file type (PDF, PPTX, DOCX, or TXT)
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  )
} 