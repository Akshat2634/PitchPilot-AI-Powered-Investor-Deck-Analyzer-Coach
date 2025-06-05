import os
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from app.services.file_service import FileService
from app.schemas.pitch_schema import PitchResponse, PitchStatus, PitchCreate, EvaluationResponse, FeedbackResponse, PitchAction, PitchData
from app.config.logging_config import setup_logging
from app.services.db_actions import DatabaseActions
from app.ai.pitch_graph import PitchGraph

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/evaluate-pitch", response_model=EvaluationResponse)
async def evaluate_pitch(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    user_query: Optional[str] = Form(None),
):
    """
    Endpoint to upload and evaluate a pitch document.
    
    Args:
        file: The pitch document file (PDF, PPTX, DOCX, TXT)
        title: Title of the pitch
        description: Optional description of the pitch
        user_query: Optional user query to evaluate / score the pitch
    
    Returns:
        PitchResponse with the created pitch details
    """
    try:
        # Use FileService to handle file upload
        file_service = FileService()
        file_content, _ = await file_service.extract_text_from_upload(file)
        logger.info(f"File content: {file_content}")
        file_path, file_type = await file_service.save_upload_file(file)
        logger.info(f"File uploaded successfully to {file_path}")
        
        # Create pitch data object
        new_pitch_data = PitchCreate(
            title=title,
            description=description,
            file_type=file_type,
            file_content=file_content
        )
        
        # Store in database using db_actions service
        db_actions = DatabaseActions()
        new_pitch = await db_actions.create_pitch(new_pitch_data, file_path)

        pitch_graph = PitchGraph()
        update_pitch_status = await db_actions.update_pitch_status(new_pitch.id, PitchStatus.PROCESSING)
        logger.info(f"Pitch status updated to: {update_pitch_status}")
        
        # Create PitchData for analysis with user query
        analysis_pitch_data = PitchData(
            pitch_text=file_content,
            user_query=user_query
        )
        
        evaluation_response = await pitch_graph.analyze_pitch(analysis_pitch_data)
        logger.info(f"Evaluation response: {evaluation_response}")
        
        # Update database with feedback and score results separately
        if evaluation_response.feedback:
            try:
                await db_actions.update_pitch_feedback_and_score(
                    pitch_id=new_pitch.id,
                    feedback=evaluation_response.feedback,
                    score=None
                )
                logger.info(f"Updated feedback for pitch {new_pitch.id}")
            except Exception as db_error:
                logger.error(f"Failed to update pitch feedback: {str(db_error)}")
                # Continue with response even if database update fails
        
        if evaluation_response.score:
            try:
                await db_actions.update_pitch_feedback_and_score(
                    pitch_id=new_pitch.id,
                    feedback=None,
                    score=evaluation_response.score
                )
                logger.info(f"Updated score for pitch {new_pitch.id}")
            except Exception as db_error:
                logger.error(f"Failed to update pitch score: {str(db_error)}")
                # Continue with response even if database update fails
        
        try:
            update_pitch_status = await db_actions.update_pitch_status(new_pitch.id, PitchStatus.COMPLETED)
            logger.info(f"Pitch status updated to: {update_pitch_status}")
        except Exception as status_error:
            logger.error(f"Failed to update pitch status to COMPLETED: {str(status_error)}")
            # Continue with response even if status update fails
            
        return EvaluationResponse(
            feedback=evaluation_response.feedback,
            score=evaluation_response.score
        )
    except HTTPException as he:
        # Update pitch status to FAILED if possible
        try:
            await db_actions.update_pitch_status(new_pitch.id, PitchStatus.FAILED)
            logger.info(f"Pitch status updated to FAILED due to HTTPException")
        except Exception as status_error:
            logger.error(f"Failed to update pitch status to FAILED: {str(status_error)}")
        raise he
    except Exception as e:
        # Update pitch status to FAILED if possible
        try:
            await db_actions.update_pitch_status(new_pitch.id, PitchStatus.FAILED)
            logger.info(f"Pitch status updated to FAILED due to exception")
        except Exception as status_error:
            logger.error(f"Failed to update pitch status to FAILED: {str(status_error)}")
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