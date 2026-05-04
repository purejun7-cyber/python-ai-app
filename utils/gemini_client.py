import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_client():
    # Streamlit Cloud の Secrets → 環境変数の順で取得
    try:
        import streamlit as st
        api_key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        api_key = ""

    if not api_key:
        api_key = (os.getenv("GEMINI_API_KEY") or "").strip()

    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.0-flash")

def generate(prompt: str) -> str:
    model = get_client()
    response = model.generate_content(prompt)
    return response.text
