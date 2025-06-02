# PitchPilot: AI-Powered Investor Pitch Analyzer & Coach

## Overview
PitchPilot is an enterprise-grade platform that leverages advanced AI to analyze and improve investor pitch decks and presentation scripts. Built with LangGraph and state-of-the-art Large Language Models, it delivers comprehensive feedback, detailed scoring, and realistic investor Q&A simulation to help founders refine and perfect their pitches for maximum impact.

## Key Features
- **Multi-dimensional Analysis**: Evaluates pitch decks across critical dimensions including clarity, market differentiation, traction evidence, and scalability potential
- **Smart Document Processing**: Seamlessly handles PDF, PPTX, DOCX, and TXT formats with advanced OCR capabilities for image-based content
- **AI-Powered Feedback**: Delivers specific, actionable suggestions based on Y Combinator and top VC best practices
- **Investor Q&A Simulation**: Generates relevant investor questions categorized by importance and provides strategic preparation guidance

## Technical Architecture
### Backend
- **Framework**: FastAPI for high-performance, async API endpoints
- **Database**: PostgreSQL with Prisma ORM for type-safe database access
- **Storage**: Supabase Storage for secure file management
- **AI/ML**: LangGraph for multi-step reasoning, OpenAI for language processing
- **Document Processing**: Advanced OCR and structured document parsing services
- **Authentication**: JWT with comprehensive role-based access control

### Data Models
- **Pitch**: Stores deck metadata, file references, and processing status
- **Feedback**: Contains detailed scoring, suggestions, and AI-generated elevator pitches
- **InvestorQuestions**: Manages categorized questions with importance ratings and rationales

## Getting Started
1. Clone the repository
2. Set up environment variables (see `.env.example`)
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   npm install
   ```
4. Initialize the database:
   ```bash
   prisma generate
   prisma db push
   ```
5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation
Once the server is running, visit `/docs` for comprehensive, interactive API documentation powered by Swagger UI.

## Development
- Robust logging system with color-coded output for easy debugging
- Async database access with context managers for reliable connections
- Type-safe schemas using Pydantic for request/response validation

## License
MIT License - See LICENSE file for details