import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.file_service import FileService
from app.schemas.pitch_schema import PitchResponse, PitchStatus, PitchCreate, EvaluationResponse, FeedbackResponse, PitchAction
from app.config.logging_config import setup_logging
from app.services.db_actions import create_pitch, get_pitch

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/evaluate-pitch", response_model=PitchResponse)
async def evaluate_pitch(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    action: PitchAction = Form(PitchAction.ANALYSIS.value) # default action is analysis
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
        logger.info(f"Evaluating pitch with action: {action}")
        logger.info(f"File: {file.filename}")
        # Use FileService to handle file upload
        file_service = FileService()
        file_path, file_type = await file_service.save_upload_file(file)
        logger.info(f"File uploaded successfully to {file_path}")
        
        # Create pitch data object
        pitch_data = PitchCreate(
            title=title,
            description=description,
            file_type=file_type
        )
        
        # Store in database using db_actions service
        new_pitch = await create_pitch(pitch_data, file_path)
            
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


# @router.get("/get-pitch/{pitch_id}", response_model=EvaluationResponse)
# async def get_pitch(pitch_id: str):
#     """
#     Endpoint to get the evaluation results for a pitch.
    
#     Args:
#         pitch_id: The ID of the pitch to get
    
#     Returns:
#         EvaluationResponse with the pitch details and evaluation results
#     """
#     try:
#         logger.info(f"Getting pitch with ID: {pitch_id}")
#         # Get pitch details from database
#         pitch = await get_pitch(pitch_id)
        
#         if not pitch:
#             raise HTTPException(status_code=404, detail="Pitch not found")
        
#         # Create pitch response
#         pitch_response = PitchResponse(
#             id=pitch.id,
#             title=pitch.title,
#             description=pitch.description,
#             file_path=pitch.filePath,
#             file_type=pitch.fileType,
#             status=pitch.status,
#             created_at=pitch.createdAt,
#             updated_at=pitch.updatedAt
#         )
        
#         # Create evaluation response
#         response = EvaluationResponse(pitch=pitch_response)
        
#         # Add feedback data if available
#         if pitch.feedback:
#             feedback_response = FeedbackResponse(
#                 id=pitch.feedback.id,
#                 pitch_id=pitch.feedback.pitchId,
#                 overall_score=pitch.feedback.overallScore,
#                 scores=pitch.feedback.scores,
#                 suggestions=pitch.feedback.suggestions,
#                 elevator_pitch=pitch.feedback.elevatorPitch,
#                 created_at=pitch.feedback.createdAt,
#                 updated_at=pitch.feedback.updatedAt
#             )
#             response.feedback = feedback_response
        
#         logger.info(f"Successfully retrieved evaluation for pitch ID: {pitch_id}")
#         return response
        
#     except HTTPException as he:
#         # Re-raise HTTP exceptions
#         raise he
#     except Exception as e:
#         logger.error(f"Error retrieving pitch evaluation: {str(e)}", exc_info=True)
#         raise HTTPException(
#             status_code=500,
#             detail="An unexpected error occurred while retrieving the pitch evaluation."
#         )