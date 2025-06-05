# PitchPilot: AI-Powered Investor Pitch Analyzer & Coach

## Overview
PitchPilot is an enterprise-grade platform that leverages advanced AI to analyze and improve investor pitch decks and presentation scripts. Built with LangGraph and state-of-the-art Large Language Models, it delivers comprehensive feedback, detailed scoring, and realistic investor Q&A simulation to help founders refine and perfect their pitches for maximum impact.

## Key Features
- **Multi-dimensional Analysis**: Evaluates pitch decks across critical dimensions including clarity, market differentiation, traction evidence, and scalability potential
- **Smart Document Processing**: Seamlessly handles PDF, PPTX, DOCX, and TXT formats with advanced OCR capabilities for image-based content
- **AI-Powered Feedback**: Delivers specific, actionable suggestions based on Y Combinator and top VC best practices
- **Investor Q&A Simulation**: Generates relevant investor questions categorized by importance and provides strategic preparation guidance

## Technical Architecture

### Backend Stack
- **Framework**: FastAPI with async support for high-performance API endpoints
- **Database**: PostgreSQL with Prisma ORM for type-safe database access
- **Storage**: Supabase Storage for secure file management
- **AI/ML**: 
  - LangGraph for multi-step reasoning workflows
  - LangChain for AI orchestration
  - OpenAI for language processing
  - Instructor for structured LLM outputs
- **Document Processing**: 
  - PyPDF2 & PDFPlumber for PDF extraction
  - python-docx for Word documents
  - python-pptx for PowerPoint presentations
- **Configuration**: Environment-based configuration with python-dotenv

### Project Structure
```
app/
├── ai/                 # AI agents and processing logic
│   ├── agents.py      # AI agent implementations
│   ├── pitch_graph.py # LangGraph workflow definitions
│   └── config.py      # AI configuration
├── api/               # FastAPI application
│   ├── api.py        # Main FastAPI app configuration
│   └── routers/      # API route handlers
│       └── pitch_api.py
├── config/           # Application configuration
│   ├── prisma_client.py
│   └── logging_config.py
├── schemas/          # Pydantic data models
│   └── pitch_schema.py
└── services/         # Business logic services
    ├── db_actions.py
    ├── file_service.py
    └── supabase_connection.py
```

### Data Models
- **Pitch**: Stores deck metadata, file references, and processing status
- **Feedback**: Contains detailed scoring, suggestions, and AI-generated elevator pitches
- **InvestorQuestions**: Manages categorized questions with importance ratings and rationales

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+ (for Prisma)
- PostgreSQL database

### Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd PitchPilot-AI-Powered-Investor-Deck-Analyzer-Coach
   ```

2. Set up environment variables:
   - Create a `.env` file in the root directory
   - Add required environment variables (DATABASE_URL, DIRECT_URL, OPENAI_API_KEY, etc.)

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Node.js dependencies:
   ```bash
   npm install
   ```

5. Initialize and migrate the database:
   ```bash
   npx prisma generate
   npx prisma db push
   ```

### Running the Application
Start the development server:
```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Documentation
Once the server is running, visit:
- **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc`
- **Health Check**: `http://localhost:8000/health`

### Main Endpoints
- `POST /evaluate-pitch` - Upload and analyze a pitch deck
- `GET /health` - API health check
- `GET /` - API information and available endpoints

## Development Features
- **Comprehensive Logging**: Color-coded logging system with configurable levels
- **Async Database Access**: Context managers for reliable database connections
- **Type Safety**: Pydantic schemas for request/response validation
- **CORS Support**: Configured for cross-origin requests
- **Error Handling**: Robust error handling throughout the application

## Dependencies
### Core Framework
- FastAPI 0.104.0+ for API framework
- Uvicorn 0.24.0+ for ASGI server
- Prisma 0.10.0+ for database ORM

### AI & ML
- OpenAI 1.3.0+ for language models
- LangChain 0.0.335+ for AI orchestration
- LangGraph 0.0.20+ for workflow management
- Instructor 1.0.0+ for structured outputs

### Document Processing
- PyPDF2 3.0.1+ for PDF processing
- python-docx 1.1.0+ for Word documents
- python-pptx 0.6.23+ for PowerPoint files
- pdfplumber 0.10.0+ for advanced PDF extraction

## License
MIT License - See LICENSE file for details