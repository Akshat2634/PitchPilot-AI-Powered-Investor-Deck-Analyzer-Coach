from app.config.prisma_client import get_prisma
from app.schemas.pitch_schema import PitchCreate, PitchStatus, FeedbackModel, ScoreModel
import logging
import json

logger = logging.getLogger(__name__)

class DatabaseActions:
    def __init__(self):
        pass

    async def create_pitch(self, pitch_data: PitchCreate, file_path: str):
        """
        Create a new pitch record in the database.
        
        Args:
            pitch_data: PitchCreate object containing pitch details
            file_path: Path where the pitch file is stored
        
        Returns:
            The created pitch record
        """
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
            return new_pitch 
        
    async def get_pitch(self, pitch_id: str):
        """
        Get a pitch record from the database by ID.
        
        Args:
            pitch_id: The ID of the pitch to get
        
        Returns:
            The pitch record
        """
        async with get_prisma() as prisma:
            pitch = await prisma.pitch.find_unique(
                where={"id": pitch_id},
                include={
                    "feedback": True,
                }
            )
            logger.info(f"Retrieved pitch with ID: {pitch_id}")
            return pitch
        

    async def update_pitch_status(self, pitch_id: str, status: PitchStatus):
        """
        Update the status of a pitch record in the database.
        
        Args:
            pitch_id: The ID of the pitch to update
            status: The new status to set
        """
        async with get_prisma() as prisma:
            updated_pitch = await prisma.pitch.update(
                where={"id": pitch_id},
                data={"status": status}
            )
            logger.info(f"Updated pitch {pitch_id} status to: {status}")
            return updated_pitch
        
    async def update_pitch_feedback_and_score(self, pitch_id: str, feedback: FeedbackModel=None, score: ScoreModel = None, pitch_content: str = None):
        """
        Update or create feedback for a pitch record in the database.
        
        Args:
            pitch_id: The ID of the pitch to update feedback for
            feedback: The feedback data to store
            score: The score data to store
            pitch_content: The elevator pitch content to store
        
        Returns:
            The updated/created feedback record
        """
        async with get_prisma() as prisma:
            # Prepare the data to update/create
            feedback_data = {}
            
            if pitch_content:
                feedback_data["elevatorPitch"] = pitch_content
            
            if score:
                feedback_data["overallScore"] = score.overall
                feedback_data["scores"] = json.dumps({
                    "clarity": {"score": score.clarity},
                    "differentiation": {"score": score.differentiation},
                    "traction": {"score": score.traction},
                    "scalability": {"score": score.scalability}
                })
            
            if feedback:
                feedback_data["suggestions"] = json.dumps({
                    "overall_feedback": feedback.overall_feedback,
                    "strengths": feedback.strengths,
                    "weaknesses": feedback.weaknesses,
                    "opportunities": feedback.opportunities,
                    "threats": feedback.threats,
                    "suggestions": feedback.suggestions
                })
            
            # Check if feedback already exists
            existing_feedback = await prisma.feedback.find_unique(
                where={"pitchId": pitch_id}
            )
            
            if existing_feedback:
                # Update existing feedback
                updated_feedback = await prisma.feedback.update(
                    where={"pitchId": pitch_id},
                    data=feedback_data
                )
                logger.info(f"Updated existing feedback for pitch {pitch_id}")
                return updated_feedback
            else:
                # Create new feedback
                new_feedback = await prisma.feedback.create(
                    data={
                        "pitchId": pitch_id,
                        **feedback_data
                    }
                )
                logger.info(f"Created new feedback for pitch {pitch_id}")
                return new_feedback
