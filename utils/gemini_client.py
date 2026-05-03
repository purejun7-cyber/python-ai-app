import os
import google.generativeai as genai
from dotenv import load_dotenv

# load_dotenv()

def get_client():
    api_key = (os.getenv("GEMINI_API_KEY") or "").strip()
    if not api_key:
        raise ValueError("GEMINI_API_KEY が .env に設定されていません")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")

def generate(prompt: str) -> str:
    model = get_client()
    response = model.generate_content(prompt)
    return response.text
