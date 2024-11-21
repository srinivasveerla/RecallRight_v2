import google.generativeai as genai
from dotenv import load_dotenv
import os
from logger_config import logger

def get_genai():
    try:
        # Load environment variables from .env file
        load_dotenv()
        GOOGLE_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

        if not GOOGLE_API_KEY:
            logger.critical("GOOGLE_GENAI_API_KEY not found in environment variables")
            return

        logger.info("Retrieved Google API Key")
        genai.configure(api_key=GOOGLE_API_KEY)

        check = list(genai.list_models())
        if check:  # Check if the list is not empty
            logger.info("Connected to GenAI successfully")
        else:
            logger.critical("GenAI Connection Failed: No models available")
            return

    except Exception as e:
        logger.critical(f"GenAI Connection Failed: {e}", exc_info=True)
        return
    else:
        return genai

if __name__ == "__main__":
    genai_instance = get_genai()
    if genai_instance:
        logger.info("GenAI instance created successfully")
