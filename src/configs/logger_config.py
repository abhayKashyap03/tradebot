import logging
import sys

def setup_logger():
    """
    Set up the root logger to output to the console.
    """
    # Define the format for our log messages
    log_format = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Set the minimum level of messages to log

    # Create a handler to write log messages to the console (stdout)
    # We use sys.stdout to ensure it works well in different environments (like Docker)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)

    # Add the handler to the root logger
    # We clear existing handlers to avoid duplicate logs in some environments
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(console_handler)