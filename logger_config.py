"""
The logging module defines the following severity levels:

    - DEBUG: Detailed information, useful for diagnosing problems.
    - INFO: Confirmation that things are working as expected.
    - WARNING: An indication of something unexpected or potential problems.
    - ERROR: A serious problem that has caused a function to fail.
    - CRITICAL: A very serious error that may stop the program.
"""
import logging

stream_handler = logging.StreamHandler()  # Default is sys.stderr
stream_handler.setLevel(logging.WARN)

# Configure the logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        stream_handler,
    ]
)

# Get the logger
logger = logging.getLogger("RecallRight_v2")
