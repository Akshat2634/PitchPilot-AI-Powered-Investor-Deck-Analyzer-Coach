import os
import logging
from supabase import create_client, Client
from dotenv import load_dotenv
from app.config.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class SupabaseConnection:
    """Simple Supabase connection management."""
    
    def __init__(self):
        """Initialize Supabase connection."""
        self.client = self._create_client()
    
    def _create_client(self) -> Client:
        """Create and return Supabase client."""
        logger.info("Initializing Supabase connection...")
        
        # Get required environment variables
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        # Validate environment variables
        if not supabase_url or not supabase_key:
            missing = []
            if not supabase_url:
                missing.append("SUPABASE_URL")
            if not supabase_key:
                missing.append("SUPABASE_KEY")
            
            error_msg = f"Missing environment variables: {', '.join(missing)}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Create client
        try:
            client = create_client(supabase_url, supabase_key)
            logger.info("Supabase client initialized successfully")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}", exc_info=True)
            raise RuntimeError(f"Failed to initialize Supabase client: {str(e)}")
    
    def get_bucket_name(self) -> str:
        """Get the Supabase bucket name from environment variables."""
        bucket_name = os.getenv("SUPABASE_BUCKET_NAME")
        if not bucket_name:
            logger.error("SUPABASE_BUCKET_NAME is not set")
            raise ValueError("SUPABASE_BUCKET_NAME environment variable is required")
        return bucket_name
    
    def test_connection(self) -> bool:
        """Test the Supabase connection."""
        try:
            self.client.auth.get_session()
            logger.info("Supabase connection test successful")
            return True
        except Exception as e:
            logger.error(f"Supabase connection test failed: {str(e)}")
            return False
        
    def download_file(self, file_path: str) -> bytes:
        """Download a file from Supabase storage."""
        try:
            file_content = self.client.storage.from_(self.bucket_name).download(file_path)
            return file_content
        except Exception as e:
            logger.error(f"Failed to download file from Supabase: {str(e)}")
            raise Exception(f"Failed to download file from Supabase: {str(e)}")
        


