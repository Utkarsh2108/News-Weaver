"""
Main File for LangGraph AgenticAI Application
---------------------------------------------
This script serves as the main entry point for running the application in different modes.
You can run the Streamlit UI, the FastAPI backend, or both concurrently.

NOTE: This script should be run from the root directory of your project.

Usage:
- To run only the Streamlit application:
  python run.py --mode streamlit

- To run only the FastAPI server on a specific port:
  python run.py --mode fastapi --port 8080

- To run both the FastAPI server and the Streamlit UI:
  python run.py --mode both
"""
# run_both.py

import threading
import uvicorn
import subprocess
import os
import time
from dotenv import load_dotenv
import sys # Import the sys module

def run_fastapi():
    """
    Runs the FastAPI application using uvicorn as a separate thread.
    """
    print("🚀 Starting FastAPI server...")
    uvicorn.run(
        "src.langgraphagenticai.api.app:app", 
        host="0.0.0.0", 
        port=8000, 
        log_level="info"
    )

def run_streamlit():
    """
    Runs the Streamlit application using subprocess.
    """
    print("🎨 Starting Streamlit UI...")
    streamlit_file = os.path.join("src", "langgraphagenticai", "main.py")
    # Set the working directory for the subprocess to the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["streamlit", "run", streamlit_file], cwd=project_root)


if __name__ == "__main__":
    # --- FIX: Add project root to Python's path ---
    # This ensures that 'src' is importable by both the main script and its subprocesses.
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    # --- END FIX ---
    
    # Load environment variables from .env file
    load_dotenv()

    # Ensure the 'News' directory exists before starting servers
    os.makedirs("News", exist_ok=True)

    # Run FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()

    # Give the FastAPI server a moment to start up before launching Streamlit
    time.sleep(3)

    # Run Streamlit in the main thread
    run_streamlit()