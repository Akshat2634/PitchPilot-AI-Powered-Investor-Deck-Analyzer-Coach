# 🚀 PitchPilot: AI-Powered Investor Deck Analyzer & Coach

> **Transform your pitch deck from good to fundable with AI-powered multi-agent analysis**

[![Built with LangGraph](https://img.shields.io/badge/Built%20with-LangGraph-blue)](https://github.com/langchain-ai/langgraph)
[![Powered by OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-green)](https://openai.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2015-black)](https://nextjs.org)

## 🎯 What is PitchPilot?

PitchPilot is an enterprise-grade AI platform that helps founders perfect their investor pitch decks. Using a sophisticated **multi-agent AI system**, it provides comprehensive analysis, actionable feedback, and investor-perspective insights to maximize your chances of securing funding.

### 🤖 Multi-Agent Orchestration

Our LangGraph-powered system employs **4 specialized AI agents** working in concert:

1. **📊 Analysis Agent** - Deep-dives into your pitch structure, narrative flow, and completeness
2. **💯 Scoring Agent** - Evaluates across 10+ dimensions using VC best practices
3. **💡 Feedback Agent** - Provides specific, actionable improvements tailored to your industry
4. **❓ Q&A Agent** - Simulates investor questions to prepare you for pitch meetings

## ✨ Core Features

### For Founders
- 🎯 **Intelligent Analysis** - Get VC-grade feedback in seconds, not weeks
- 📈 **Comprehensive Scoring** - Know exactly where your pitch stands (0-100 scale)
- 💬 **Investor Q&A Simulation** - Prepare for tough questions before they're asked
- 📄 **Multi-Format Support** - Upload PDF, PPTX, DOCX, or TXT files
- 🎨 **Beautiful Dashboard** - Modern UI to visualize your pitch performance

### Technical Excellence
- ⚡ **Real-time Processing** - Async architecture for lightning-fast analysis
- 🔐 **Enterprise Security** - Secure file handling with Supabase storage
- 🎭 **Smart Routing** - LangGraph orchestrates agent workflows intelligently
- 📊 **Structured Output** - Type-safe responses with Pydantic validation

## 🏗️ Architecture Overview

```mermaid
graph LR
    A[Frontend - Next.js] --> B[FastAPI Backend]
    B --> C[LangGraph Orchestrator]
    C --> D[Analysis Agent]
    C --> E[Scoring Agent]
    C --> F[Feedback Agent]
    C --> G[Q&A Agent]
    D --> H[OpenAI]
    E --> H
    F --> H
    G --> H
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+ & Node.js 16+
- PostgreSQL database
- OpenAI API key
- Supabase account (for storage)

### 1️⃣ Clone & Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/PitchPilot-AI-Powered-Investor-Deck-Analyzer-Coach.git
cd PitchPilot-AI-Powered-Investor-Deck-Analyzer-Coach

# Setup Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Setup Node.js dependencies
npm install
```

### 2️⃣ Environment Configuration

Create `.env` in the root directory:

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/pitchpilot"
DIRECT_URL="postgresql://user:password@localhost:5432/pitchpilot"

# OpenAI
OPENAI_API_KEY="sk-..."

# Supabase
NEXT_PUBLIC_SUPABASE_URL="https://xxx.supabase.co"
NEXT_PUBLIC_SUPABASE_ANON_KEY="xxx"
SUPABASE_SERVICE_ROLE_KEY="xxx"
```

### 3️⃣ Database Setup

```bash
# Generate Prisma client
npx prisma generate

# Push schema to database
npx prisma db push
```

### 4️⃣ Launch the Platform

```bash
# Terminal 1: Start the backend
cd backend
python main.py

# Terminal 2: Start the frontend
cd frontend
pnpm run dev
```

🎉 **Visit [http://localhost:3000](http://localhost:3000) to start analyzing!**

## 📁 Project Structure

```
PitchPilot/
├── 🎨 frontend/                 # Next.js 15 React application
│   ├── src/
│   │   ├── app/                # App router pages
│   │   ├── components/         # React components
│   │   ├── lib/               # API client & utilities
│   │   └── types/             # TypeScript definitions
│   └── public/                # Static assets
│
├── 🧠 backend/                 # FastAPI + LangGraph backend
│   ├── app/
│   │   ├── ai/               # Multi-agent system
│   │   │   ├── agents.py     # Agent implementations
│   │   │   └── pitch_graph.py # LangGraph workflows
│   │   ├── api/              # API endpoints
│   │   ├── schemas/          # Pydantic models
│   │   └── services/         # Business logic
│   └── main.py               # Application entry
│
└── 📊 prisma/                  # Database schema
    └── schema.prisma
```

## 🤖 The AI Agents Explained

### 🔍 Analysis Agent
Examines your pitch deck for:
- Problem-solution fit clarity
- Market opportunity presentation
- Team credibility signals
- Business model viability

### 📊 Scoring Agent
Rates your pitch on:
- **Clarity** (0-100): How well you communicate your idea
- **Market Differentiation** (0-100): Your competitive advantage
- **Traction Evidence** (0-100): Proof of concept/growth
- **Scalability** (0-100): Growth potential
- **Team Strength** (0-100): Founder-market fit

### 💡 Feedback Agent
Provides:
- Specific improvement suggestions
- Industry-tailored recommendations
- Before/after examples
- Priority action items

### ❓ Q&A Agent
Generates:
- Top 10 likely investor questions
- Difficulty ratings (Easy/Medium/Hard)
- Suggested answer frameworks
- Red flag identifications

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15.3.3 with App Router
- **UI**: React 19 + Tailwind CSS
- **Language**: TypeScript
- **Icons**: Lucide React

### Backend
- **API**: FastAPI with async/await
- **AI Orchestration**: LangGraph + LangChain
- **LLM**: OpenAI GPT-4
- **Database**: PostgreSQL + Prisma ORM
- **Storage**: Supabase Storage

### DevOps
- **Logging**: Color-coded console output
- **Testing**: Pytest + Jest
- **API Docs**: Auto-generated Swagger/ReDoc

## 📚 API Reference

### Main Endpoints

#### `POST /evaluate-pitch`
Upload and analyze a pitch deck

**Request:**
```multipart/form-data
- file: PDF/PPTX/DOCX/TXT (max 10MB)
- pitch_title: string
- description: string (optional)
- user_query: string (AI analysis prompt)
```

**Response:**
```json
{
  "pitch_id": "uuid",
  "status": "completed",
  "scores": {
    "overall_score": 85,
    "clarity_score": 90,
    "market_differentiation_score": 80,
    ...
  },
  "feedback": {
    "strengths": ["..."],
    "weaknesses": ["..."],
    "suggestions": ["..."],
    "elevator_pitch": "..."
  },
  "investor_questions": [...]
}
```

## 🚦 Development Workflow

1. **Local Development**
   ```bash
   # Backend hot-reload
   cd backend && python main.py
   
   # Frontend with hot-reload
   cd frontend && pnpm run dev
   ```

2. **Database Migrations**
   ```bash
   npx prisma migrate dev --name your_migration_name
   ```

3. **Type Generation**
   ```bash
   npx prisma generate
   ```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

Built with ❤️ for founders by founders, powered by:
- [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- [OpenAI](https://openai.com) for language models
- [Next.js](https://nextjs.org) for the frontend framework
- [FastAPI](https://fastapi.tiangolo.com) for the backend API

---

<p align="center">
  <strong>Ready to perfect your pitch?</strong><br>
  <a href="http://localhost:3000">🚀 Start Analyzing Now</a>
</p>