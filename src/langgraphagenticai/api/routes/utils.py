# src/langgraphagenticai/api/routes/utils.py

from fastapi import APIRouter, HTTPException
from src.langgraphagenticai.api.schemas.models import TranslationRequest, TranslationResponse
from src.langgraphagenticai.api.core.dependencies import initialize_llm
from src.langgraphagenticai.tools.translation_tool import SUPPORTED_LANGUAGES, create_translation_tool

router = APIRouter()

@router.get("/", summary="API Root")
async def root():
    return {"message": "Welcome to the LangGraph AgenticAI API"}

@router.get("/health", summary="Health Check")
async def health_check():
    return {"status": "healthy"}

@router.get("/languages", summary="Get Supported Languages")
async def get_supported_languages():
    return {"supported_languages": SUPPORTED_LANGUAGES}

@router.post("/translate", response_model=TranslationResponse, summary="Translate Text")
async def translate_text(request: TranslationRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text to translate cannot be empty.")
    if request.target_language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.target_language}")
    
    llm = initialize_llm(request.model)
    translation_tool = create_translation_tool(llm)
    try:
        translated_text = translation_tool._run(request.text, request.target_language)
        return TranslationResponse(success=True, translated_text=translated_text, target_language=request.target_language, message="Text successfully translated")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")