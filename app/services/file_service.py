# app/services/file_service.py
import os
import logging
from fastapi import UploadFile, HTTPException
from typing import Tuple
import uuid
from app.config.logging_config import setup_logging
from app.services.supabase_connection import SupabaseConnection

# Setup logging
setup_logging() 
logger = logging.getLogger(__name__)


class FileService:
    def __init__(self):
        """Initialize FileService instance."""
        self.supabase_connection = SupabaseConnection()
        self.supabase = self.supabase_connection.client
        self.bucket_name = self.supabase_connection.get_bucket_name()
    
    def get_file_type(self, filename: str) -> str:
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
    
    async def save_upload_file(self, file: UploadFile) -> Tuple[str, str]:
        """
        Save uploaded file to Supabase storage and return file path and type.
        
        Returns:
            Tuple[str, str]: (file_path, file_type)
        """
        logger.info(f"Processing file upload: {file.filename}")
        file_type = self.get_file_type(file.filename)
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}.{file_type}"
        logger.debug(f"Generated unique filename: {unique_filename}")
        
        # Read file content
        file_content = await file.read()
        logger.debug(f"Read file content, size: {len(file_content)} bytes")
        
        # Upload to Supabase Storage
        try:
            logger.info(f"Uploading file to Supabase bucket: {self.bucket_name}")
            result = self.supabase.storage.from_(self.bucket_name).upload(
                unique_filename,
                file_content,
                {"content-type": file.content_type}
            )
            
            # Get the public URL
            file_path = self.supabase.storage.from_(self.bucket_name).get_public_url(unique_filename)
            logger.info(f"File uploaded successfully. Path: {file_path}")
            
            return file_path, file_type
            
        except Exception as e:
            logger.error(f"Failed to upload file to Supabase: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to upload file to Supabase: {str(e)}"
            )