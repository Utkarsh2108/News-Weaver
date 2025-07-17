# src/langgraphagenticai/api/core/dependencies.py

import os
from fastapi import HTTPException
from typing import Optional
from src.langgraphagenticai.LLMS.groqllm import GroqLLM

def initialize_llm(model: str = "llama3-8b-8192"):
    """Initializes and returns Groq LLM instance using API key from environment."""
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(status_code=500, detail="GROQ_API_KEY not found in environment variables.")
    try:
        user_controls = {"GROQ_API_KEY": os.getenv("GROQ_API_KEY"), "selected_groq_model": model}
        return GroqLLM(user_contols_input=user_controls).get_llm_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize LLM: {str(e)}")

def check_tool_keys():
    """Checks for required tool API keys in environment variables."""
    if not os.getenv("TAVILY_API_KEY"):
        raise HTTPException(status_code=500, detail="TAVILY_API_KEY not found for web search or news.")

def check_email_credentials(recipient_email: Optional[str]):
    """Checks for email credentials if an email is to be sent."""
    if recipient_email and not (os.getenv("GMAIL_SENDER_EMAIL") and os.getenv("GMAIL_SENDER_PASSWORD")):
        raise HTTPException(status_code=400, detail="Email credentials (GMAIL_SENDER_EMAIL, GMAIL_SENDER_PASSWORD) must be set in the .env file to send emails.")   