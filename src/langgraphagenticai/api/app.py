# src/langgraphagenticai/api/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.langgraphagenticai.api.routes import chat, news, utils

# Load environment variables at the start
load_dotenv()

app = FastAPI(
    title="News Weaver",
    description="An API for a news agent, a web-enabled chatbot, and a basic chatbot."
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers from the different route files
app.include_router(utils.router, tags=["Utility"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(news.router, prefix="/news", tags=["News & Files"])