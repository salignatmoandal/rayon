import os
import logging
from datetime import datetime

def setup_logger() -> logging.Logger:
    """
    Sets up the logger for the application.

    This function ensures that a log directory exists and creates a file handler
    that writes logs to a file in the specified directory. The log file is named
    based on the current date (e.g., '2025-02-13.log').

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Set the log directory relative to the current working directory.
    # This avoids using an absolute path (e.g., '/app/logs') which might be read-only.
    log_dir = os.path.join(os.getcwd(), 'logs')
    # Build the log file name using the current date.
    log_file = os.path.join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log')

    # Ensure that the log directory exists. If it doesn't, create it.
    os.makedirs(log_dir, exist_ok=True)

    # Create a logger instance; here we use the root logger.
    logger = logging.getLogger()
    # Set the logging level to DEBUG so that all messages are captured.
    logger.setLevel(logging.DEBUG)

    # Create a file handler to write log messages to the log file.
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Create a console handler to output log messages to the console.
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Define a formatter that includes the timestamp, logger name, level, and message.
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Apply the formatter to both handlers.
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add both handlers to the logger.
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger