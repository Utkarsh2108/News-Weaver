# 📰 News Weaver

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-FastAPI%20%7C%20Streamlit-green)

Welcome to News Weaver, a sophisticated, agentic AI application designed to be your personal information hub. Built with a powerful backend using Python, LangGraph, and FastAPI, News Weaver provides a suite of intelligent tools for fetching, summarizing, and interacting with information in real-time.

## ✨ Key Features

News Weaver is more than just a chatbot; it's a multi-agent system designed for diverse information-gathering tasks.

* **🤖 Multi-Agent System**: At its core, News Weaver allows you to switch between three distinct AI agents, each tailored for a specific purpose:
    1.  **News Agent**: Your personal intelligence analyst. This agent automates the entire news-gathering workflow. It fetches articles from the web based on your topic, creates concise summaries, translates them into different languages, and delivers the final report as a PDF to your email.
    2.  **Web-Enabled Chatbot**: An advanced conversationalist that overcomes the knowledge cut-off limitations of standard LLMs. It uses the **Tavily Search API** to access real-time information from the internet, providing accurate and up-to-date answers to your questions.
    3.  **Basic Chatbot**: A fast, general-purpose chatbot for quick questions and creative tasks. It relies entirely on the LLM's vast internal knowledge and is powered by the high-speed **Groq** inference engine.

* **📰 Intelligent News Processing**:
    * **Natural Language Queries**: Interact with the News Agent naturally. Ask for news like *"get me the latest tech news in German"* or *"what happened in the stock market this week?"*, and the system will parse your request to execute the task.
    * **Multi-Language Support**: Break down language barriers. The integrated translation tool can convert news summaries into over 20 languages, making global information accessible.
    * **Automated Delivery**: The agent automatically saves all summaries as both Markdown and PDF files. If you provide an email address, it will send the portable PDF summary directly to your inbox.


## ⚙️ **How to Use the Application**
The Streamlit interface is designed for ease of use.

1. **Select a Usecase**: Use the sidebar to choose between `News`, `Chatbot With Web`, or `Basic Chatbot`.

2. **For the News Agent**:

 - **Sidebar Controls**: Use the dropdowns and text fields to select a time frame, topic, and language. Optionally, enter an email to receive the PDF summary. Click "Fetch & Send News".

- **Chat Input**: Alternatively, type a natural language query into the main chat box (e.g., "show me this week's climate news") and press Enter.

3. **For Chatbots**:

- Select the desired chatbot from the sidebar.

- Type your message or question into the chat input at the bottom of the page and press Enter.

## 🛠️ Technology Stack & Architecture

News Weaver operates as two cooperative services, providing a clear separation between the core logic and the user interface.

1.  **FastAPI Backend**: The brain of the operation. It exposes all AI functionalities through a REST API and handles graph execution, tool calls (Tavily, Translation), file processing (PDF generation), and email dispatch.
2.  **Streamlit Frontend**: The face of the application. It provides an intuitive web interface for users to interact with the different AI agents. It makes requests to the FastAPI backend to execute tasks and displays the results.

## 🚀 Getting Started
Follow these steps to get News Weaver running on your local machine.

1. **Installation**
1. **Clone the repository**:
```
git clone https://github.com/Utkarsh2108/News-Weaver.git
```

2. Create and activate a virtual environment:
```
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```
3. **Install the required dependencies**:
We recommend creating a `requirements.txt` file for easy installation.you can simply run:
```
pip install -r requirements.txt
```
4. **Set up your environment variables**:
Create a file named `.env `in the root directory of the project and add your API keys.
```
# .env.example

# Required for the LLM
GROQ_API_KEY="gsk_..."

# Required for the News and Web-Enabled Chatbot agents
TAVILY_API_KEY="tvly-..."

# Optional: Required only for the email functionality
GMAIL_SENDER_EMAIL="your_email@gmail.com"
GMAIL_SENDER_PASSWORD="your_google_app_password"
```
Note: For `GMAIL_SENDER_PASSWORD`, you need to generate an "App Password" from your Google Account security settings if you have 2-Factor Authentication enabled.

2. **Running the Application**
Execute the following command from the project's root directory:
```
  # To run only the Streamlit application:
  python run.py --mode streamlit

  # To run only the FastAPI server on a specific port:
  python run.py --mode fastapi --port 8080

  # To run both the FastAPI server and the Streamlit UI:
  python run.py --mode both
```

## 📂 **Project Structure**
The project is organized into a src directory to maintain a clean and scalable structure.
```
.
├── .env                  # Environment variables (API keys)
├── requirements.txt      # Python dependencies
├── run_both.py           # Main script to launch the application
└── src/
    └── langgraphagenticai/
        ├── api/            # All FastAPI related code
        │   ├── core/
        │   ├── routes/
        │   ├── schemas/
        │   └── app.py
        ├── graph/          # LangGraph graph definitions
        ├── LLMS/           # LLM configurations (e.g., Groq)
        ├── nodes/          # Logic for individual nodes in the graph
        ├── state/          # State definitions for the graphs
        ├── tools/          # Custom tools (e.g., PDF, email)
        ├── ui/             # Streamlit UI components
        ├── utils/          # Utility functions (e.g., message parser)
        └── main.py         # Entry point for the Streamlit app
```