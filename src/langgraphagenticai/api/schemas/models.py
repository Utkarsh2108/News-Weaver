# src/langgraphagenticai/api/schemas/models.py

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List

class BaseRequest(BaseModel):
    model: str = Field("llama3-8b-8192", description="The model to use for the LLM.")

class NewsRequest(BaseRequest):
    frequency: str = Field("daily", description="News frequency: daily, weekly, monthly, yearly.")
    topic: str = Field("general news", description="The topic for the news.")
    language: str = Field("English", description="The target language for the summary.")
    recipient_email: Optional[str] = Field(None, description="Optional email address to send the PDF summary to.")

class NewsInvokeRequest(BaseRequest):
    query: str = Field(..., description="A natural language query for the news agent.")
    recipient_email: Optional[str] = Field(None, description="Optional email address to send the PDF summary to.")

class ChatRequest(BaseModel):
    message: str

class WebChatRequest(BaseRequest):
    message: str

class TranslationRequest(BaseRequest):
    text: str
    target_language: str

class NewsResponse(BaseModel):
    success: bool
    message: str
    filename: Optional[str] = None
    file_path: Optional[str] = None
    processing_details: Optional[Dict[str, Any]] = None

class ChatResponse(BaseModel):
    success: bool
    response: str

class WebChatResponse(ChatResponse):
    tool_outputs: Optional[List[Any]] = None

class TranslationResponse(BaseModel):
    success: bool
    translated_text: Optional[str] = None
    target_language: str
    message: str