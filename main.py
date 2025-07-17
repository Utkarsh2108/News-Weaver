# main.py

import uvicorn
import os

from src.langgraphagenticai.api import app

if __name__ == "__main__":
    # Ensure the 'News' directory exists
    os.makedirs("News", exist_ok=True)
    # Note: The host is set to "0.0.0.0" to be accessible on your network
    uvicorn.run(app, host="0.0.0.0", port=8000)