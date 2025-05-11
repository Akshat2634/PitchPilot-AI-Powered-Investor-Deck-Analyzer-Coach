import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.file_service import FileService
from app.schemas.pitch import PitchResponse, PitchStatus, PitchCreate
from app.config.logging_config import setup_logging
from app.config.prisma_client import get_prisma

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/evaluate", response_model=PitchResponse)
async def evaluate_pitch(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None)
):
    """
    Endpoint to upload and evaluate a pitch document.
    
    Args:
        file: The pitch document file (PDF, PPTX, DOCX, TXT)
        title: Title of the pitch
        description: Optional description of the pitch
    
    Returns:
        PitchResponse with the created pitch details
    """
    try:
        # Use FileService to handle file upload
        file_path, file_type = await FileService.save_upload_file(file)
        logger.info(f"File uploaded successfully to {file_path}")
        
        # Create pitch data object
        pitch_data = PitchCreate(
            title=title,
            description=description,
            file_type=file_type
        )
        
        # Store in database
        async with get_prisma() as prisma:
            new_pitch = await prisma.pitch.create(
                data={
                    "title": pitch_data.title,
                    "description": pitch_data.description,
                    "filePath": file_path,
                    "fileType": pitch_data.file_type,
                    "status": PitchStatus.PENDING
                }
            )
            
            logger.info(f"Pitch created with ID: {new_pitch.id}")
            
            # Here you would typically trigger an async task to process the pitch
            # For now, we'll just return the created pitch
            
            return PitchResponse(
                id=new_pitch.id,
                title=new_pitch.title,
                description=new_pitch.description,
                file_path=new_pitch.filePath,
                file_type=new_pitch.fileType,
                status=new_pitch.status,
                created_at=new_pitch.createdAt,
                updated_at=new_pitch.updatedAt
            )
            
    except HTTPException as he:
        # Re-raise HTTP exceptions as they are already properly formatted
        raise he
    except Exception as e:
        logger.error(f"Error processing pitch upload: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing your pitch. Please try again later."
        )

