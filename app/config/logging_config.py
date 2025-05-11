import logging
import sys
from colorama import Fore, Style, init

# Initialize colorama
init()

class ColoredFormatter(logging.Formatter):
    """Custom formatter with colored output"""
    
    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        # Store the original level name
        levelname = record.levelname
        
        # Add color to the level name
        if levelname in self.COLORS:
            # Color the level name
            record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
            # Color the message using the original level name
            record.msg = f"{self.COLORS[levelname]}{record.msg}{Style.RESET_ALL}"
        
        return super().format(record)

def setup_logging():
    """Configure logging with colored output"""
    # Get the root logger
    root_logger = logging.getLogger()
    
    # Only setup logging if no handlers exist
    if not root_logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # Configure root logger
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(console_handler)
        
        # Configure specific loggers
        loggers = [
            'app',
            'app.services',
            'app.api',
            'app.core'
        ]
        
        for logger_name in loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(logging.DEBUG)
            logger.propagate = False 