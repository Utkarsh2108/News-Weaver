# src/langgraphagenticai/tools/translation_tool.py

from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from typing import Type, Any
from pydantic import BaseModel, Field

class TranslationInput(BaseModel):
    """Input for translation tool"""
    text: str = Field(description="Text to translate")
    target_language: str = Field(description="Target language for translation")

class TranslationTool(BaseTool):
    """Tool for translating text to different languages"""
    
    name: str = "translate_text"
    description: str = "Translate text to a specified language"
    args_schema: Type[BaseModel] = TranslationInput
    llm: Any = Field(description="Language model for translation")  # Add llm as a field
    
    def _run(self, text: str, target_language: str) -> str:
        """
        Translate text to target language using LLM
        """
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", f"""You are a professional translator. Translate the following text to {target_language}.
            
            **Instructions:**
            1. Maintain the original formatting (markdown, headers, links, etc.)
            2. Preserve all URLs and links as they are
            3. Keep the structure intact (dates, bullet points, etc.)
            4. Translate only the content, not the markdown syntax
            5. If translating news, maintain journalistic tone
            6. For technical terms, provide the translation with original term in parentheses if needed
            
            **Important:**
            - Keep all markdown formatting symbols (###, **, [], (), etc.)
            - Don't translate URLs or source names unless specifically requested
            - Maintain the same paragraph structure
            """),
            ("user", "Text to translate:\n{text}")
        ])
        
        try:
            response = self.llm.invoke(prompt_template.format(text=text))
            return response.content
        except Exception as e:
            return f"Translation error: {str(e)}"

def create_translation_tool(llm):
    """Create and return translation tool"""
    return TranslationTool(llm=llm)

# Language options for the UI
SUPPORTED_LANGUAGES = {
    'English': 'English',
    'Hindi': 'Hindi (हिंदी)',
    'Spanish': 'Spanish (Español)',
    'French': 'French (Français)',
    'German': 'German (Deutsch)',
    'Italian': 'Italian (Italiano)',
    'Portuguese': 'Portuguese (Português)',
    'Russian': 'Russian (Русский)',
    'Japanese': 'Japanese (日本語)',
    'Korean': 'Korean (한국어)',
    'Chinese': 'Chinese (中文)',
    'Arabic': 'Arabic (العربية)',
    'Bengali': 'Bengali (বাংলা)',
    'Tamil': 'Tamil (தமிழ்)',
    'Telugu': 'Telugu (తెలుగు)',
    'Marathi': 'Marathi (मराठी)',
    'Gujarati': 'Gujarati (ગુજરાતી)',
    'Punjabi': 'Punjabi (ਪੰਜਾਬੀ)',
    'Urdu': 'Urdu (اردو)',
    'Malayalam': 'Malayalam (മലയാളം)',
    'Kannada': 'Kannada (ಕನ್ನಡ)',
    'Dutch': 'Dutch (Nederlands)',
    'Swedish': 'Swedish (Svenska)',
    'Norwegian': 'Norwegian (Norsk)',
    'Thai': 'Thai (ไทย)',
    'Vietnamese': 'Vietnamese (Tiếng Việt)'
}