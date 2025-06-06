'use client'

import React, { useState, useEffect, useRef } from 'react';
import { 
  Upload, 
  BarChart3, 
  MessageSquare, 
  CheckCircle, 
  Star,
  ArrowRight,
  FileText,
  Users,
  Brain,
  Sparkles,
  PlayCircle,
  X,
  Menu
} from 'lucide-react';
import { useRouter } from 'next/navigation';

const PitchPilotEnterprise = () => {
  const router = useRouter();
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeFeature, setActiveFeature] = useState(0);
  const [isVideoModalOpen, setIsVideoModalOpen] = useState(false);
  const heroRef = useRef(null);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveFeature(prev => (prev + 1) % 3);
    }, 4000);
    return () => clearInterval(timer);
  }, []);

  // Floating animation for hero elements
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in-up');
          }
        });
      },
      { threshold: 0.1 }
    );

    const elements = document.querySelectorAll('.animate-on-scroll');
    elements.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: "Multi-Agent AI System",
      description: "Specialized AI agents work in orchestrated workflows using LangGraph architecture",
      color: "from-blue-500 to-purple-600"
    },
    {
      icon: <BarChart3 className="w-8 h-8" />,
      title: "Intelligent Agent Routing",
      description: "Smart supervisor routes tasks between analysis, scoring, and Q&A simulation agents",
      color: "from-purple-500 to-pink-600"
    },
    {
      icon: <MessageSquare className="w-8 h-8" />,
      title: "Collaborative Agent Network",
      description: "Agents collaborate to deliver comprehensive feedback and realistic investor preparation",
      color: "from-pink-500 to-red-600"
    }
  ];

  const stats = [
    { number: "95%", label: "Agent Accuracy", description: "Multi-agent precision rate" },
    { number: "3x", label: "Faster Processing", description: "Through parallel agent execution" },
    { number: "500+", label: "Successful Pitches", description: "Refined by our agent network" },
    { number: "4", label: "Specialized Agents", description: "Working in orchestrated workflows" }
  ];

  const testimonials = [
    {
      name: "Sarah Chen",
      role: "CEO, TechFlow AI",
      company: "Series A Startup",
      content: "The multi-agent system is incredible. Each agent brought unique insights - the analysis agent caught nuances I missed, while the scoring agent provided quantified validation. Game-changing for pitch prep.",
      rating: 5,
      avatar: "SC"
    },
    {
      name: "Marcus Rodriguez",
      role: "Founder, GreenTech Solutions",
      company: "Seed Stage",
      content: "Watching the agents collaborate through LangGraph was fascinating. The supervisor intelligently routed my requests, and each specialized agent delivered expert-level feedback.",
      rating: 5,
      avatar: "MR"
    },
    {
      name: "Emily Watson",
      role: "Co-founder, FinanceHub",
      company: "Series B",
      content: "The orchestrated workflow of multiple AI agents working together produces analysis that rivals top-tier VC feedback. The depth and coordination is remarkable.",
      rating: 5,
      avatar: "EW"
    }
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-white overflow-hidden">
      {/* Navigation */}
      <nav className="fixed top-0 left-0 right-0 z-50 bg-slate-950/80 backdrop-blur-xl border-b border-slate-800/50">
        <div className="max-w-7xl mx-auto px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                PitchPilot
              </span>
            </div>

            {/* Desktop Navigation */}
            <div className="hidden lg:flex items-center">
              <button 
                onClick={() => router.push('/upload')}
                className="px-6 py-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200 transform hover:scale-105"
              >
                Get Started
              </button>
            </div>

            {/* Mobile menu button */}
            <button 
              className="lg:hidden p-2"
              onClick={() => setIsMenuOpen(!isMenuOpen)}
            >
              {isMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>

          {/* Mobile Navigation */}
          {isMenuOpen && (
            <div className="lg:hidden absolute top-16 left-0 right-0 bg-slate-900/95 backdrop-blur-xl border-b border-slate-800/50 p-6">
              <div className="flex justify-center">
                <button 
                  onClick={() => router.push('/upload')}
                  className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200"
                >
                  Get Started
                </button>
              </div>
            </div>
          )}
        </div>
      </nav>

      {/* Hero Section */}
      <section ref={heroRef} className="relative pt-24 pb-32 px-6 lg:px-8 overflow-hidden">
        {/* Animated background */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-purple-900/20 to-pink-900/20"></div>
        <div className="absolute inset-0">
          <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-500/10 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        </div>

        <div className="relative max-w-7xl mx-auto">
          <div className="text-center animate-on-scroll">
            <div className="inline-flex items-center px-4 py-2 bg-blue-500/20 rounded-full border border-blue-500/30 mb-8">
              <Sparkles className="w-4 h-4 text-blue-400 mr-2" />
              <span className="text-sm text-blue-300 font-medium">AI-Powered Pitch Analysis</span>
            </div>
            
            <h1 className="text-5xl lg:text-7xl font-bold mb-6 bg-gradient-to-r from-white via-blue-100 to-purple-200 bg-clip-text text-transparent">
              Perfect Your{' '}
              <span className="bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                Investor Pitch
              </span>{' '}
              with AI
            </h1>
            
            <p className="text-xl lg:text-2xl text-slate-300 mb-12 max-w-4xl mx-auto leading-relaxed">
              Transform your investor presentations with our multi-agent AI system. Specialized agents collaborate 
              to deliver world-class analysis, comprehensive scoring, and realistic investor Q&A simulation.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-16">
              <button 
                onClick={() => router.push('/upload')}
                className="group px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/25 text-lg font-semibold"
              >
                Start Free Analysis
                <ArrowRight className="w-5 h-5 ml-2 inline-block group-hover:translate-x-1 transition-transform duration-200" />
              </button>
              
              <button 
                className="group px-8 py-4 bg-slate-800/50 border border-slate-700/50 rounded-xl hover:bg-slate-700/50 transition-all duration-300 text-lg font-semibold flex items-center"
                onClick={() => setIsVideoModalOpen(true)}
              >
                <PlayCircle className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform duration-200" />
                Watch Demo
              </button>
            </div>

            {/* Feature highlights */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {features.map((feature, index) => (
                <div 
                  key={index}
                  className={`p-6 rounded-2xl bg-slate-800/30 border border-slate-700/50 hover:bg-slate-800/50 transition-all duration-300 transform hover:scale-105 ${
                    activeFeature === index ? 'ring-2 ring-blue-500/50' : ''
                  }`}
                >
                  <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${feature.color} flex items-center justify-center mb-4 mx-auto`}>
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold mb-2 text-white">{feature.title}</h3>
                  <p className="text-slate-400 leading-relaxed">{feature.description}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-6 lg:px-8 bg-slate-900/50">
        <div className="max-w-7xl mx-auto">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center animate-on-scroll">
                <div className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                  {stat.number}
                </div>
                <div className="text-lg font-semibold text-slate-200 mb-1">{stat.label}</div>
                <div className="text-sm text-slate-400">{stat.description}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-32 px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20 animate-on-scroll px-4">
            <h2 className="text-4xl lg:text-5xl font-bold mb-6 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent leading-tight">
              Multi-Agent AI Architecture
            </h2>
            <p className="text-xl text-slate-400 max-w-4xl mx-auto leading-relaxed px-2">
              Orchestrated AI agents powered by LangGraph work together to deliver comprehensive pitch analysis
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mb-20">
            <div className="animate-on-scroll">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center mb-6">
                <Brain className="w-8 h-8" />
              </div>
              <h3 className="text-3xl font-bold mb-4 text-white">Intelligent Agent Orchestration</h3>
              <p className="text-lg text-slate-400 mb-6 leading-relaxed">
                Our multi-agent system uses LangGraph to orchestrate specialized AI agents. Each agent has unique 
                expertise - analysis, scoring, Q&A simulation - working together seamlessly for comprehensive results.
              </p>
              <ul className="space-y-3">
                {['Supervisor Agent for intelligent routing', 'Analysis Agent for detailed feedback', 'Scoring Agent for quantitative evaluation', 'Workflow state management'].map((item, index) => (
                  <li key={index} className="flex items-center text-slate-300">
                    <CheckCircle className="w-5 h-5 text-green-400 mr-3 flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div className="relative animate-on-scroll">
              <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700/50">
                <div className="text-center mb-6">
                  <h4 className="text-lg font-semibold text-white mb-2">Agent Workflow</h4>
                  <div className="text-sm text-slate-400">LangGraph Orchestration</div>
                </div>
                
                {/* Agent Flow Visualization */}
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-blue-500/10 rounded-lg border border-blue-500/20">
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-blue-400 rounded-full mr-3"></div>
                      <span className="text-blue-300 font-medium">Supervisor Agent</span>
                    </div>
                    <div className="text-xs text-slate-400">Routing</div>
                  </div>
                  
                  <div className="flex justify-center">
                    <div className="w-px h-6 bg-slate-600"></div>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-purple-500/10 rounded-lg border border-purple-500/20">
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-purple-400 rounded-full mr-3"></div>
                      <span className="text-purple-300 font-medium">Analysis Agent</span>
                    </div>
                    <div className="text-xs text-slate-400">Processing</div>
                  </div>
                  
                  <div className="flex justify-center">
                    <div className="w-px h-6 bg-slate-600"></div>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-green-500/10 rounded-lg border border-green-500/20">
                    <div className="flex items-center">
                      <div className="w-3 h-3 bg-green-400 rounded-full mr-3"></div>
                      <span className="text-green-300 font-medium">Scoring Agent</span>
                    </div>
                    <div className="text-xs text-slate-400">Complete</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <div className="relative animate-on-scroll lg:order-2">
              <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700/50">
                <h4 className="text-xl font-semibold mb-6 text-white">Agent Specialization</h4>
                <div className="space-y-6">
                  <div className="p-4 bg-blue-500/10 rounded-xl border border-blue-500/20">
                    <div className="flex items-center mb-2">
                      <Brain className="w-5 h-5 text-blue-400 mr-2" />
                      <span className="text-blue-300 font-semibold">Analysis Agent</span>
                    </div>
                    <p className="text-slate-400 text-sm">Generates detailed feedback using VC frameworks from Y Combinator and top firms</p>
                  </div>
                  <div className="p-4 bg-purple-500/10 rounded-xl border border-purple-500/20">
                    <div className="flex items-center mb-2">
                      <BarChart3 className="w-5 h-5 text-purple-400 mr-2" />
                      <span className="text-purple-300 font-semibold">Scoring Agent</span>
                    </div>
                    <p className="text-slate-400 text-sm">Provides quantitative evaluation across multiple dimensions with detailed justification</p>
                  </div>
                  <div className="p-4 bg-green-500/10 rounded-xl border border-green-500/20">
                    <div className="flex items-center mb-2">
                      <MessageSquare className="w-5 h-5 text-green-400 mr-2" />
                      <span className="text-green-300 font-semibold">Q&A Agent</span>
                    </div>
                    <p className="text-slate-400 text-sm">Simulates realistic investor questions for comprehensive pitch preparation</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="animate-on-scroll lg:order-1">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-purple-500 to-pink-600 flex items-center justify-center mb-6">
                <Users className="w-8 h-8" />
              </div>
              <h3 className="text-3xl font-bold mb-4 text-white">Specialized Agent Expertise</h3>
              <p className="text-lg text-slate-400 mb-6 leading-relaxed">
                Each AI agent is fine-tuned for specific tasks, ensuring expert-level performance. The supervisor 
                intelligently routes requests to the most appropriate agent based on user needs and workflow state.
              </p>
              <ul className="space-y-3">
                {['Domain-specific agent training', 'Intelligent task routing', 'Collaborative workflow execution', 'State-aware decision making', 'Comprehensive result synthesis'].map((item, index) => (
                  <li key={index} className="flex items-center text-slate-300">
                    <CheckCircle className="w-5 h-5 text-green-400 mr-3 flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Add Smart Document Processing section */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mt-32">
            <div className="animate-on-scroll">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-green-500 to-teal-600 flex items-center justify-center mb-6">
                <Upload className="w-8 h-8" />
              </div>
              <h3 className="text-3xl font-bold mb-4 text-white">Smart Document Processing</h3>
              <p className="text-lg text-slate-400 mb-6 leading-relaxed">
                Upload any format - PDF, PPTX, DOCX, or TXT. Our advanced OCR and document parsing 
                technology extracts content with 99% accuracy, feeding clean data to our agent network.
              </p>
              <ul className="space-y-3">
                {['Advanced OCR for image-based content', 'Multi-format support', 'Instant processing', 'Secure document handling'].map((item, index) => (
                  <li key={index} className="flex items-center text-slate-300">
                    <CheckCircle className="w-5 h-5 text-green-400 mr-3 flex-shrink-0" />
                    {item}
                  </li>
                ))}
              </ul>
            </div>
            <div className="relative animate-on-scroll">
              <div className="bg-slate-800/50 rounded-2xl p-8 border border-slate-700/50">
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center">
                    <FileText className="w-6 h-6 text-blue-400 mr-3" />
                    <span className="text-slate-300">pitch-deck-v2.pdf</span>
                  </div>
                  <div className="w-3 h-3 bg-green-400 rounded-full"></div>
                </div>
                <div className="space-y-4">
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-blue-400 rounded-full mr-3"></div>
                    <span className="text-slate-400">Extracting text content...</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-purple-400 rounded-full mr-3"></div>
                    <span className="text-slate-400">Processing images and charts...</span>
                  </div>
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-green-400 rounded-full mr-3"></div>
                    <span className="text-slate-400">Routing to agent network ✓</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-32 px-6 lg:px-8 bg-slate-900/30">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20 animate-on-scroll">
            <h2 className="text-4xl lg:text-5xl font-bold mb-6 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
              Trusted by Top Founders
            </h2>
            <p className="text-xl text-slate-400 max-w-3xl mx-auto">
              See how PitchPilot has helped startups secure funding and perfect their presentations
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {testimonials.map((testimonial, index) => (
              <div key={index} className="bg-slate-800/30 rounded-2xl p-8 border border-slate-700/50 hover:bg-slate-800/50 transition-all duration-300 animate-on-scroll">
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-current" />
                  ))}
                </div>
                <p className="text-slate-300 mb-6 leading-relaxed">&ldquo;{testimonial.content}&rdquo;</p>
                <div className="flex items-center">
                  <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-semibold mr-4">
                    {testimonial.avatar}
                  </div>
                  <div>
                    <div className="text-white font-semibold">{testimonial.name}</div>
                    <div className="text-slate-400 text-sm">{testimonial.role}</div>
                    <div className="text-slate-500 text-xs">{testimonial.company}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center animate-on-scroll">
          <h2 className="text-4xl lg:text-5xl font-bold mb-6 bg-gradient-to-r from-white to-slate-300 bg-clip-text text-transparent">
            Ready to Perfect Your Pitch?
          </h2>
          <p className="text-xl text-slate-400 mb-12 leading-relaxed">
            Join hundreds of successful founders who&apos;ve refined their pitches with enterprise-grade AI analysis
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-6">
            <button 
              onClick={() => router.push('/upload')}
              className="group px-8 py-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl hover:from-blue-600 hover:to-purple-700 transition-all duration-300 transform hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/25 text-lg font-semibold"
            >
              Start Free Trial
              <ArrowRight className="w-5 h-5 ml-2 inline-block group-hover:translate-x-1 transition-transform duration-200" />
            </button>
            {/* <button className="px-8 py-4 bg-slate-800/50 border border-slate-700/50 rounded-xl hover:bg-slate-700/50 transition-all duration-300 text-lg font-semibold">
              Schedule Demo
            </button> */}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 px-6 lg:px-8 border-t border-slate-800/50">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col lg:flex-row items-center justify-between">
            <div className="flex items-center space-x-3 mb-8 lg:mb-0">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              <span className="text-xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                PitchPilot
              </span>
            </div>
            <div className="text-slate-400 text-sm">
              Made with ❤️ for founders
            </div>
          </div>
          
          <div className="mt-8 text-center">
            <p className="text-slate-400 text-sm lg:text-base max-w-4xl mx-auto leading-relaxed">
              Enterprise-grade AI platform for analyzing and improving investor pitch decks. Perfect your pitch with advanced AI feedback and scoring.
            </p>
          </div>
          
          <div className="text-center text-slate-500 text-sm mt-6">
            © 2025 PitchPilot. All rights reserved. Built with enterprise-grade AI.
          </div>
        </div>
      </footer>

      {/* Video Modal */}
      {isVideoModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
          <div className="relative w-full max-w-4xl mx-4">
            <button 
              className="absolute -top-12 right-0 text-white hover:text-slate-300 transition-colors duration-200"
              onClick={() => setIsVideoModalOpen(false)}
            >
              <X className="w-8 h-8" />
            </button>
            <div className="bg-slate-900 rounded-2xl p-8 text-center">
              <PlayCircle className="w-24 h-24 text-blue-400 mx-auto mb-6" />
              <h3 className="text-2xl font-bold text-white mb-4">Demo Video</h3>
              <p className="text-slate-400 mb-6">Watch how PitchPilot transforms investor presentations</p>
              <div className="bg-slate-800 rounded-xl p-12 text-slate-500">
                <div className="flex flex-col items-center space-y-4">
                  <div className="flex items-center space-x-2">
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                    <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
                    <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
                  </div>
                  <span className="text-lg font-medium bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
                    Demo video coming soon...
                  </span>
                  <p className="text-sm text-slate-400">
                    Get ready to see PitchPilot in action
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        @keyframes fade-in-up {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
        
        .animate-fade-in-up {
          animation: fade-in-up 0.6s ease-out forwards;
        }
        
        .animate-on-scroll {
          opacity: 0;
          transform: translateY(30px);
          transition: all 0.6s ease-out;
        }
        
        .animate-on-scroll.animate-fade-in-up {
          opacity: 1;
          transform: translateY(0);
        }
      `}</style>
    </div>
  );
};

export default PitchPilotEnterprise; 