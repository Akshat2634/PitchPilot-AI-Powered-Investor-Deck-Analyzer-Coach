# 🚀 PitchPilot: AI-Powered Investor Deck Analyzer & Coach

> **Transform your pitch deck from good to fundable with AI-powered multi-agent analysis**

[![Built with LangGraph](https://img.shields.io/badge/Built%20with-LangGraph-blue)](https://github.com/langchain-ai/langgraph)
[![Powered by OpenAI](https://img.shields.io/badge/Powered%20by-OpenAI-green)](https://openai.com)
[![Next.js](https://img.shields.io/badge/Frontend-Next.js%2015-black)](https://nextjs.org)

## 🎯 What is PitchPilot?

PitchPilot is an enterprise-grade AI platform that helps founders perfect their investor pitch decks. Using a sophisticated **multi-agent AI system**, it provides comprehensive analysis, actionable feedback, and investor-perspective insights to maximize your chances of securing funding.

<img width="1347" alt="Screenshot 2025-06-05 at 11 05 23 PM" src="https://github.com/user-attachments/assets/a5ff5402-8258-4b15-b946-17efd4b2a2ac" />

### 🤖 Multi-Agent Orchestration

<img width="1347" alt="Screenshot 2025-06-05 at 11 05 37 PM" src="https://github.com/user-attachments/assets/6ce777ae-1357-4dde-b6f0-da8023018836" />

Our LangGraph-powered system employs **3 specialized AI agents** working in concert:

1. **🧠 Supervisor Agent** - OpenAI-powered workflow orchestrator that intelligently routes tasks between agents
2. **📊 Analysis Agent** - Deep-dives into your pitch structure, narrative flow, and completeness using VC frameworks
3. **💯 Scoring Agent** - Evaluates across 5 key dimensions: clarity, differentiation, traction, scalability, and overall rating

## ✨ Core Features

### For Founders
- **Intelligent Analysis** - Get VC-grade feedback in seconds, not weeks
- 📈 **Comprehensive Scoring** - Know exactly where your pitch stands (0-10 scale)
- 💬 **Smart Workflow Routing** - AI supervisor determines what analysis you need based on your query
- 📄 **Multi-Format Support** - Upload PDF, PPTX, DOCX, or TXT files
- 📊 **Professional Dashboard** - Modern UI to visualize your pitch performance

<img width="1347" alt="Screenshot 2025-06-05 at 11 05 51 PM" src="https://github.com/user-attachments/assets/94d362cd-5a77-454a-a509-916501130f42" />

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
    C --> D[Supervisor Agent]
    D --> E[Analysis Agent]
    D --> F[Scoring Agent]
    E --> G[OpenAI]
    F --> G
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ & Node.js 16+
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

# Setup Node.js dependencies (using pnpm)
npm install -g pnpm
pnpm install
```

### 2️⃣ Environment Configuration

Create `.env` in the backend folder:

```env
# Database
DATABASE_URL="postgresql://user:password@localhost:5432/pitchpilot"
DIRECT_URL="postgresql://user:password@localhost:5432/pitchpilot"

# OpenAI
OPENAI_API_KEY="sk-..."
OPENAI_MODEL="gpt-4.1-mini"
OPENAI_MODEL_SUPERVISOR="gpt-4.1"

# Supabase
SUPABASE_URL="https://xxx.supabase.co"
SUPABASE_KEY="xxx"
```

Create .env in the frontend folder

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_NAME=PitchPilot
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
├── 🎨 frontend/                 # Next.js 15.3.3 React application
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
│   │   │   ├── pitch_graph.py # LangGraph workflows
│   │   │   └── config.py     # AI configuration
│   │   ├── api/              # API endpoints
│   │   │   ├── api.py        # FastAPI app configuration
│   │   │   └── routers/      # Route handlers
│   │   │       └── pitch_api.py
│   │   ├── config/           # Application configuration
│   │   │   ├── prisma_client.py
│   │   │   └── logging_config.py
│   │   ├── schemas/          # Pydantic models
│   │   │   └── pitch_schema.py
│   │   └── services/         # Business logic
│   │       ├── db_actions.py
│   │       ├── file_service.py
│   │       └── supabase_connection.py
│   └── main.py               # Application entry
│
└── 📊 prisma/                  # Database schema
    └── schema.prisma
```

## 🤖 The AI Agents Explained

<img width="1347" alt="Screenshot 2025-06-05 at 11 05 48 PM" src="https://github.com/user-attachments/assets/51742024-1637-4784-9de8-0dbdffa00ec0" />

### 🧠 Supervisor Agent
- **OpenAI-powered workflow orchestrator**
- Analyzes user queries to determine optimal agent routing
- Implements smart fallback logic for robust operation
- Routes between analysis and scoring based on user needs

### 🔍 Analysis Agent
Examines your pitch deck using VC frameworks for:
- **Problem-solution fit clarity** using Y Combinator standards
- **Market opportunity presentation** with a16z evaluation criteria
- **Team credibility signals** based on top-tier VC best practices
- **Business model viability** assessment

### 📊 Scoring Agent
Provides quantitative evaluation across 5 key dimensions:
- **Clarity** (0-10): How well you communicate your idea
- **Differentiation** (0-10): Your competitive advantage strength
- **Traction** (0-10): Proof of concept/growth evidence
- **Scalability** (0-10): Growth and expansion potential
- **Overall** (0-10): Comprehensive pitch strength

### 🎯 Q&A Simulation Agent
Generates mock investor questions from your deck:
- **Coming Soon** - Intelligent question generation based on your pitch content
- Simulates real investor meeting scenarios
- Helps you prepare for tough questions before the actual pitch
- Identifies potential weak spots that investors might probe

## 🛠️ Tech Stack

### Frontend
- **Framework**: Next.js 15.3.3 with App Router
- **UI**: React 19 + Tailwind CSS 4
- **Language**: TypeScript 5
- **Icons**: Lucide React 0.513.0
- **Package Manager**: pnpm

### Backend
- **API**: FastAPI 0.104.0+ with async/await
- **AI Orchestration**: LangGraph 0.0.20+ + LangChain 0.0.335+
- **LLM**: OpenAI 1.3.0+
- **Database**: PostgreSQL + Prisma ORM 0.10.0+
- **Storage**: Supabase 2.0.0+

### Document Processing
- **PDF**: PyPDF2 3.0.1+ & pdfplumber 0.10.0+
- **Word**: python-docx 1.1.0+
- **PowerPoint**: python-pptx 0.6.23+
- **Structured Output**: instructor 1.0.0+

## 📚 API Reference

### Main Endpoints

#### `POST /evaluate-pitch`
Upload and analyze a pitch deck

**Request:**
```multipart/form-data
- file: PDF/PPTX/DOCX/TXT (max 10MB)
- title: string (pitch title)
- description: string (optional pitch description)
- user_query: string (AI analysis prompt - what you want analyzed)
```

**Response:**
```json
{
  "feedback": {
    "overall_feedback": "Your pitch demonstrates...",
    "strengths": "Strong market opportunity...",
    "weaknesses": "Limited traction evidence...",
    "opportunities": "Consider expanding...",
    "threats": "Potential competitive risks...",
    "suggestions": "Prioritized improvement steps..."
  },
  "score": {
    "clarity": 8.5,
    "differentiation": 7.2,
    "traction": 6.8,
    "scalability": 8.0,
    "overall": 7.6
  }
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
