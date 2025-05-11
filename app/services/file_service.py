# app/services/file_service.py
import os
import logging
from fastapi import UploadFile, HTTPException
from typing import Tuple
from supabase import create_client, Client
import uuid
from dotenv import load_dotenv
from app.config.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Supabase client with proper error handling
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = os.getenv("SUPABASE_BUCKET_NAME")

# Validate required environment variables
if not SUPABASE_URL or not SUPABASE_KEY or not BUCKET_NAME:
    missing_vars = []
    if not SUPABASE_URL:
        logger.error("SUPABASE_URL is not set")
        missing_vars.append("SUPABASE_URL")
    if not SUPABASE_KEY:
        logger.error("SUPABASE_KEY is not set")
        missing_vars.append("SUPABASE_KEY")
    if not BUCKET_NAME:
        logger.error("SUPABASE_BUCKET_NAME is not set")
        missing_vars.append("SUPABASE_BUCKET_NAME")
    raise ValueError(f"Required environment variable(s) missing: {', '.join(missing_vars)}")

# Initialize Supabase client
try:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("Supabase client initialized successfully")
    
    # Verify connection by getting session (lightweight operation)
    session = supabase.auth.get_session()
    logger.info("Supabase authentication session retrieved")
    
except Exception as e:
    logger.error(f"Failed to initialize Supabase client: {str(e)}")
    raise RuntimeError(f"Failed to initialize Supabase client: {str(e)}")


class FileService:
    @staticmethod
    def get_file_type(filename: str) -> str:
        """Extract file type from filename."""
        logger.debug(f"Extracting file type from filename: {filename}")
        extension = os.path.splitext(filename)[1].lower()
        
        if extension == ".pdf":
            logger.debug(f"File type detected: pdf")
            return "pdf"
        elif extension == ".pptx":
            logger.debug(f"File type detected: pptx")
            return "pptx"
        elif extension == ".docx":
            logger.debug(f"File type detected: docx")
            return "docx"
        elif extension == ".txt":
            logger.debug(f"File type detected: txt")
            return "txt"
        else:
            logger.warning(f"Unsupported file type: {extension}")
            raise HTTPException(
                status_code=400, 
                detail="Unsupported file type. Supported types: pdf, pptx, docx, txt"
            )
    
    @staticmethod
    async def save_upload_file(file: UploadFile) -> Tuple[str, str]:
        """
        Save uploaded file to Supabase storage and return file path and type.
        
        Returns:
            Tuple[str, str]: (file_path, file_type)
        """
        logger.info(f"Processing file upload: {file.filename}")
        file_type = FileService.get_file_type(file.filename)
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.{file_type}"
        logger.debug(f"Generated unique filename: {unique_filename}")
        
        # Read file content
        file_content = await file.read()
        logger.debug(f"Read file content, size: {len(file_content)} bytes")
        
        # Upload to Supabase Storage
        try:
            logger.info(f"Uploading file to Supabase bucket: {BUCKET_NAME}")
            result = supabase.storage.from_(BUCKET_NAME).upload(
                unique_filename,
                file_content,
                {"content-type": file.content_type}
            )
            
            # Get the public URL
            file_path = supabase.storage.from_(BUCKET_NAME).get_public_url(unique_filename)
            logger.info(f"File uploaded successfully. Path: {file_path}")
            
            return file_path, file_type
            
        except Exception as e:
            logger.error(f"Failed to upload file to Supabase: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to Supabase: {str(e)}"
            )