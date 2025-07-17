# src/langgraphagenticai/ui/streamlitui/loadui.py

import streamlit as st
import os
from dotenv import load_dotenv
from src.langgraphagenticai.ui.uiconfigfile import Config
from src.langgraphagenticai.tools.translation_tool import SUPPORTED_LANGUAGES

load_dotenv()

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def load_streamlit_ui(self):
        st.set_page_config(page_title="🤖 " + self.config.get_page_title(), layout="wide")
        
        # Initialize session state
        st.session_state.setdefault('IsFetchButtonClicked', False)

        with st.sidebar:
            st.header("⚙️ Controls")
            self.user_controls["selected_llm"] = "Groq"
            self.user_controls["selected_groq_model"] = "llama3-70b-8192"
            self.user_controls["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")
            
            usecase_options = self.config.get_usecase_options()
            self.user_controls["selected_usecase"] = st.selectbox("Select a Usecase", usecase_options)

            if self.user_controls["selected_usecase"] in ["Chatbot With Web", "News"]:
                self.user_controls["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")

            # --- News-specific UI in sidebar ---
            if self.user_controls['selected_usecase'] == "News":
                st.subheader("📰 News Explorer Settings")
                time_frame = st.selectbox("📅 Select Time Frame", ["Daily", "Weekly", "Monthly", "Yearly"])
                news_topic = st.text_input("📝 Enter News Topic", help="Leave empty for general news.")
                target_language = st.selectbox("🗣️ Select Output Language", options=list(SUPPORTED_LANGUAGES.keys()))
                recipient_email = st.text_input("📧 Email PDF To", help="Enter an email to send the PDF summary.")

                if st.button("🔍 Fetch & Send News", use_container_width=True, disabled=not self.user_controls["TAVILY_API_KEY"]):
                    st.session_state.IsFetchButtonClicked = True
                    st.session_state.timeframe = time_frame
                    st.session_state.news_topic = news_topic or "general news"
                    st.session_state.target_language = target_language
                    st.session_state.recipient_email = recipient_email
                    st.success("🚀 Starting news process...")
        
        # --- Main Page Content ---
        st.header("🤖 " + self.config.get_page_title())
        st.subheader(f"Usecase: {self.user_controls['selected_usecase']}")

        # --- Display Usecase Descriptions ---
        if self.user_controls["selected_usecase"] == "Basic Chatbot":
            st.markdown("""
            A simple conversational AI that relies solely on the LLM's internal knowledge to answer your questions.
            - **Simple Q&A:** Ask general questions.
            - **No External Tools:** Does not search the web.
            - **Quick Responses:** Ideal for straightforward queries.
            """)
        elif self.user_controls["selected_usecase"] == "Chatbot With Web":
            st.markdown("""
            An advanced chatbot that can search the web for up-to-date information to answer your questions.
            - **Web Search:** Uses Tavily Search to find current information.
            - **Tool Integration:** Demonstrates how an AI can use external tools.
            - **Fact-Based Answers:** Provides answers based on the latest web data.
            """)
        elif self.user_controls["selected_usecase"] == "News":
            st.markdown("""
            A news agent that fetches, summarizes, and translates the latest news on a topic of your choice. It can also convert the summary to a PDF and email it to you.
            - **Custom News Feeds:** Get news for any topic and time frame.
            - **Multi-language Support:** Translate summaries into various languages.
            - **PDF & Email:** Delivers a portable PDF summary directly to your inbox.
            """)
            
        return self.user_controls