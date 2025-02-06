import logging
import os 
from datetime import datetime
from utils.config import LOG_DIR

def setup_logger(name: str= __name__) -> logging.Logger:
    """
    Setup a logger with a specific name.
    Args: Name of the logger.
    Returns: Logger.
    """

    # Create a logger
    os.makedirs(LOG_DIR, exist_ok=True)

    # Configure the logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Create a file handler
    file_handler = logging.FileHandler(os.path.join(LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log"))
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    file_handler.setLevel(logging.DEBUG)

    # Create a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    stream_handler.setLevel(logging.DEBUG)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
    
    