import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import pitch_api
from app.config.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)


# Create FastAPI app
app = FastAPI(
    title="AI-Powered Investor Pitch Analyzer",
    description="API for analyzing investor pitch decks and generating feedback",
    version="0.1.0"
)

logger.info(f"Initialized FastAPI app: {app.title} v{app.version}")

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pitch_api.router)


@app.get("/health")
async def health():
    logger.debug("Health check endpoint called")
    return {"status": "healthy and running"}

@app.get("/")
async def root():
    logger.debug("Root endpoint called")
    return {
        "message": "Welcome to the AI-Powered Investor Pitch Analyzer API",
        "version": "0.1.0",
        "endpoints": [
            {"path": "/api/evaluate-pitch", "method": "POST", "description": "Upload and analyze a pitch deck"},
            {"path": "/api/evaluate-pitch/{pitch_id}", "method": "GET", "description": "Get evaluation results"},
            {"path": "/api/simulate-QnA/{pitch_id}", "method": "POST", "description": "Generate investor questions"},
            {"path": "/api/simulate-QnA/{pitch_id}", "method": "GET", "description": "Get generated investor questions"}
        ]
    }
