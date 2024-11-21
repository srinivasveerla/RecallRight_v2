import google.generativeai as genai

from dotenv import load_dotenv
import os

def get_genai():
    load_dotenv()  # Load environment variables from .env file

    GOOGLE_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
    # print(GOOGLE_API_KEY)

    genai.configure(api_key=GOOGLE_API_KEY)

    for m in genai.list_models():
        if "embedContent" in m.supported_generation_methods:
            print(m.name)

    return genai
if __name__ == "__main__":
    get_genai()