from app.config.prisma_client import get_prisma
from app.schemas.pitch_schema import PitchCreate, PitchStatus, FeedbackModel, ScoreModel
import logging

logger = logging.getLogger(__name__)

class DatabaseActions:
    def __init__(self):
        self.prisma = get_prisma()

    async def create_pitch(self, pitch_data: PitchCreate, file_path: str):
        """
        Create a new pitch record in the database.
        
        Args:
            pitch_data: PitchCreate object containing pitch details
            file_path: Path where the pitch file is stored
        
        Returns:
            The created pitch record
        """
        async with self.prisma as prisma:
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
        async with self.prisma as prisma:
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
        async with self.prisma as prisma:
            updated_pitch = await prisma.pitch.update(
                where={"id": pitch_id},
                data={"status": status}
            )
            logger.info(f"Updated pitch {pitch_id} status to: {status}")
            return updated_pitch
        
    async def update_pitch_feedback_and_score(self, pitch_id: str, feedback: FeedbackModel=None, score: ScoreModel = None):
        """
        Update or create feedback for a pitch record in the database.
        
        Args:
            pitch_id: The ID of the pitch to update feedback for
            feedback: The feedback data to store
            score: The score data to store
        
        Returns:
            The updated/created feedback record
        """
        async with self.prisma as prisma:
            # Prepare the data to update/create
            feedback_data = {}
            
            if score:
                feedback_data["overallScore"] = score.overall
                feedback_data["scores"] = {
                    "clarity": {"score": score.clarity, "explanation": ""},
                    "differentiation": {"score": score.differentiation, "explanation": ""},
                    "traction": {"score": score.traction, "explanation": ""},
                    "scalability": {"score": score.scalability, "explanation": ""}
                }
            
            if feedback:
                feedback_data["suggestions"] = {
                    "overall_feedback": feedback.overall_feedback,
                    "strengths": feedback.strengths,
                    "weaknesses": feedback.weaknesses,
                    "opportunities": feedback.opportunities,
                    "threats": feedback.threats,
                    "suggestions": feedback.suggestions
                }
            
            # Try to update existing feedback, or create new one
            updated_feedback = await prisma.feedback.upsert(
                where={"pitchId": pitch_id},
                data=feedback_data,
                create={
                    "pitchId": pitch_id,
                    **feedback_data
                }
            )
            
            logger.info(f"Updated feedback for pitch {pitch_id}")
            return updated_feedback
