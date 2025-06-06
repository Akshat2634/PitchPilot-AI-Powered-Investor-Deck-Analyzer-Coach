import logging
import os
from typing import Optional, Dict
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from app.config.logging_config import setup_logging
from typing_extensions import TypedDict
from app.schemas.pitch_schema import FeedbackModel, ScoreModel, PitchData
from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion
import instructor
from langgraph.graph import MessagesState


# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

load_dotenv()

class ConfigError(Exception):
    """Custom exception for configuration errors"""
    pass

async def parse_openai_response(response: ChatCompletion) -> str:
    """
    Parse the content from an OpenAI ChatCompletion response.
    
    Args:
        response (ChatCompletion): The response from OpenAI API
        
    Returns:
        str: The extracted message content
    """
    return response.choices[0].message.content


async def get_api_key() -> str:
    """
    Retrieve OpenAI API key from environment variables.

    Returns:
        str: The OpenAI API key

    Raises:
        ConfigError: If API key is not found
    """
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key is None:
            raise ConfigError(
                "OPENAI_API_KEY not found in environment variables or Streamlit secrets"
            )
        return api_key
    except Exception as e:
        logger.error(f"Failed to retrieve OpenAI API key: {str(e)}")
        raise ConfigError(f"Failed to retrieve OpenAI API key: {str(e)}")


async def get_openai_client() -> AsyncOpenAI:
    """
    Create and configure a LangChain OpenAI chat model.

    Returns:
        ChatOpenAI: Configured LLM instance

    Raises:
        ConfigError: If API key cannot be loaded
    """
    try:
        api_key = await get_api_key()
        os.environ["OPENAI_API_KEY"] = api_key
        logger.info(f"OpenAI API key loaded successfully")
        client = instructor.from_openai(AsyncOpenAI(api_key=api_key))
        return client
    except Exception as e:
        logger.error(f"Failed to create LLM: {str(e)}")
        raise ConfigError(f"Failed to initialize language model: {str(e)}")






# AI-Powered Investor Pitch Analyzer & Coach
# Concept: Founders upload pitch decks or scripts, and the system provides feedback using LLM-based reasoning.
# Unique Angles: • LanGraph to score across dimensions: clarity, differentiation, traction, scalability. • Upload slide decks or transcripts → Convert to text (OCR or parsing). • Multi-node LangGraph to: • Evaluate against YC/VC best practices • Suggest slide-level edits - QnA
# API Ideas: • /evaluate-pitch: Upload + Score + Suggestions • /simulate-QnA: Generate mock investor questions from your deck
# "

