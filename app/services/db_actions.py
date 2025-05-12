from app.config.prisma_client import get_prisma
from app.schemas.pitch_schema import PitchCreate, PitchStatus
import logging

logger = logging.getLogger(__name__)

async def create_pitch(pitch_data: PitchCreate, file_path: str):
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
    
async def get_pitch(pitch_id: str):
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