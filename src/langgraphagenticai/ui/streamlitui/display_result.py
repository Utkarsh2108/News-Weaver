# src/langgraphagenticai/ui/streamlitui/display_result.py

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class DisplayResultStreamlit:
    def __init__(self, usecase, graph, user_message):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase = self.usecase
        graph = self.graph
        user_message = self.user_message
        print(f"DisplayResult - Usecase: {usecase}, Message: {user_message}")

        # Validate all required API keys before proceeding with any use case logic
        if not self._validate_api_keys():
            return

        if usecase == "Basic Chatbot":
            self._handle_basic_chatbot(graph, user_message)
            
        elif usecase == "Chatbot With Web":
            self._handle_chatbot_with_web(graph, user_message)
            
        elif usecase == "News":
            self._handle_news(graph, user_message)

    def _validate_api_keys(self):
        """Validate that all required API keys are present for the selected use case."""
        is_valid = True
        
        # Check GROQ API key (always required as it's the default LLM)
        if not os.getenv("GROQ_API_KEY"):
            st.error("❌ GROQ API key is missing from .env file. Please add GROQ_API_KEY to your .env file.")
            st.info("💡 Get your GROQ API key from: https://console.groq.com/keys")
            is_valid = False
        
        # Check TAVILY API key if required for the selected use case
        if self.usecase in ["Chatbot With Web", "News"]:
            if not os.getenv("TAVILY_API_KEY"):
                st.error(f"❌ TAVILY API key is missing from .env file. It's required for '{self.usecase}'.")
                st.info("💡 Get your TAVILY API key from: https://app.tavily.com/home")
                is_valid = False
        
        return is_valid

    def _handle_basic_chatbot(self, graph, user_message):
        """Handle basic chatbot interaction"""
        try:
            with st.chat_message("user"):
                st.write(user_message)
            with st.spinner("Thinking..."):
                for event in graph.stream({'messages': ("user", user_message)}):
                    print(event.values())
                    for value in event.values():
                        if "messages" in value and value["messages"].content:
                            with st.chat_message("assistant"):
                                st.write(value["messages"].content)
        except Exception as e:
            st.error(f"❌ Error in basic chatbot: {str(e)}")
            self._show_troubleshooting_basic()

    def _handle_chatbot_with_web(self, graph, user_message):
        """Handle chatbot with web search capabilities"""
        try:
            # Prepare state and invoke the graph
            initial_state = {"messages": [("user", user_message)]} # Ensure initial state is a list of tuples for LangChain
            
            with st.chat_message("user"):
                st.write(user_message)

            with st.spinner("🔍 Searching the web for information..."):
                res = graph.invoke(initial_state)
            
            for message in res['messages']:
                if isinstance(message, HumanMessage):
                    # Already displayed, but good for completeness if message structure changes
                    pass 
                elif isinstance(message, ToolMessage):
                    with st.chat_message("ai"):
                        st.write("🔍 **Tool Call Start**")
                        # ToolMessage content is often JSON or string, display appropriately
                        try:
                            tool_output = json.loads(message.content)
                            st.json(tool_output)
                        except json.JSONDecodeError:
                            st.write(message.content)
                        st.write("🔍 **Tool Call End**")
                elif isinstance(message, AIMessage) and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
                        
        except Exception as e:
            error_msg = str(e).lower()
            if "unauthorized" in error_msg or "api key" in error_msg:
                st.error("❌ API key error: Please check your TAVILY API key in .env file.")
                st.info("💡 Make sure you've added a valid TAVILY_API_KEY to your .env file.")
            else:
                st.error(f"❌ Error in web chatbot: {str(e)}")
            self._show_troubleshooting_web()

# Other methods in the class remain the same
    def _handle_news(self, graph, user_message):
        """Handle news fetching, display, and download options."""
        try:
            parts = user_message.split(':')
            # The frequency here is capitalized, e.g., "Daily"
            frequency, topic, target_language, *_ = parts + ["general news", "English"]
            topic = topic or "general news"
            
            status_text = f"Fetching and summarizing **{topic}** news"
            if target_language.lower() != 'english':
                status_text += f" in **{target_language}**... ⏳"
            else:
                status_text += "... ⏳"

            with st.spinner(status_text):
                # Invoke the graph to perform all backend operations
                graph.invoke({"messages": [("user", user_message)]})
                
                # --- Generate File Paths ---
                topic_clean = topic.replace(' ', '_').replace('/', '_')
                lang_suffix = ""
                if target_language.lower() != 'english':
                    lang_suffix = f"_{target_language.replace(' ', '_').replace('(', '').replace(')', '')}"
                
                # --- FIX: Convert frequency to lowercase to match the saved filename ---
                base_filename = f"{frequency.lower()}_{topic_clean}{lang_suffix}_summary"
                
                md_path = f"./News/{base_filename}.md"
                pdf_path = f"./News/{base_filename}.pdf"

                # --- Display Results ---
                if not os.path.exists(md_path):
                    st.error(f"❌ News file not found: {md_path}")
                    st.info("🔄 The news fetching process may have failed. Please try again.")
                    return

                with open(md_path, "r", encoding='utf-8') as file:
                    markdown_content = file.read()

                st.success(f"✅ **{topic.title()}** news summary is ready!")
                st.markdown(markdown_content, unsafe_allow_html=True)

                # --- Download Buttons ---
                st.write("---")
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="📥 Download Summary (.md)",
                        data=markdown_content,
                        file_name=f"{base_filename}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with col2:
                    if os.path.exists(pdf_path):
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="📄 Download Summary (.pdf)",
                                data=pdf_file.read(),
                                file_name=f"{base_filename}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
        
        except Exception as e:
            # The existing exception handling logic remains the same
            st.error(f"❌ An error occurred while processing the news: {str(e)}")
            self._show_troubleshooting_news()


    def _show_troubleshooting_basic(self):
        """Show troubleshooting for basic chatbot"""
        with st.expander("🔧 Troubleshooting - Basic Chatbot"):
            st.write("**Possible solutions:**")
            st.write("1. Check your LLM API key (GROQ) in .env file")
            st.write("2. Verify your internet connection")
            st.write("3. Try a simpler message")
            st.write("4. Check the application logs for more details")

    def _show_troubleshooting_web(self):
        """Show troubleshooting for web chatbot"""
        with st.expander("🔧 Troubleshooting - Web Chatbot"):
            st.write("**Possible solutions:**")
            st.write("1. **Check TAVILY API key:** Ensure it's valid and added to .env file")
            st.write("2. **Verify internet connection:** Web search requires internet access")
            st.write("3. **Try simpler queries:** Complex queries might timeout")
            st.write("4. **Check API limits:** You might have exceeded your API quota")
            st.write("5. **Test with basic query:** Try 'What is the weather today?'")

    def _show_troubleshooting_news(self):
        """Show troubleshooting for news"""
        with st.expander("🔧 Troubleshooting - News"):
            st.write("**Possible solutions:**")
            st.write("1. **API Key Issues:**")
            st.write("   - Verify your TAVILY API key is valid in .env file")
            st.write("   - Check if you have API quota remaining")
            st.write("   - Try regenerating your API key")
            st.write("2. **Connection Issues:**")
            st.write("   - Check your internet connection")
            st.write("   - Try again in a few minutes")
            st.write("3. **Topic Issues:**")
            st.write("   - Try a different news topic")
            st.write("   - Use simpler keywords")
            st.write("4. **System Issues:**")
            st.write("   - Ensure the 'News' directory exists in your project root.")
            st.write("   - Restart the application")

    def _format_news_topic(self, topic):
        """Format news topic for display"""
        if topic.lower() == "general news":
            return "General News"
        return topic.title()

    def _get_language_display_name(self, language):
        """Get display name for language"""
        try:
            from src.langgraphagenticai.tools.translation_tool import SUPPORTED_LANGUAGES
            return SUPPORTED_LANGUAGES.get(language, language)
        except ImportError:
            return language

