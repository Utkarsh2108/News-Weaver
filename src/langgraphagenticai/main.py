# src/langgraphagenticai/main.py
import streamlit as st
from src.langgraphagenticai.ui.streamlitui.loadui import LoadStreamlitUI
from src.langgraphagenticai.LLMS.groqllm import GroqLLM
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.ui.streamlitui.display_result import DisplayResultStreamlit
from src.langgraphagenticai.utils.message_parser import NewsMessageParser

def load_langgraph_agenticai_app():
    """
    Loads and runs the LangGraph AgenticAI application with a streamlined and
    efficient main execution flow.
    """
    ui = LoadStreamlitUI()
    user_input = ui.load_streamlit_ui()
    
    user_message = None
    detected_usecase = user_input.get("selected_usecase")

    # --- Path 1: User clicks the button in the sidebar ---
    if st.session_state.get('IsFetchButtonClicked', False):
        user_message = (
            f"{st.session_state.timeframe}:{st.session_state.news_topic}:"
            f"{st.session_state.target_language}:{st.session_state.get('recipient_email', '')}"
        )
        # Ensure the usecase is set to News when the button is clicked
        detected_usecase = "News"

    # --- Path 2: User types in the chat input box ---
    else:
        chat_input = st.chat_input("Enter your message for the selected usecase:")
        if chat_input:
            if detected_usecase == "News":
                parser = NewsMessageParser()
                # First, check if the input looks like a news request
                if parser.is_news_request(chat_input):
                    with st.spinner("Analyzing your request..."):
                        parsed = parser.parse_news_message(chat_input)
                        user_message = parsed['formatted_message']
                        st.info(f"🔍 Understood! Fetching: **{parsed['frequency']} | {parsed['topic']} | {parsed['language']}**")
                else:
                    # If not a news request, inform the user and do nothing
                    st.warning("This doesn't look like a news request. Please try asking for news or use the sidebar controls.", icon="⚠️")
            else:
                # For other usecases (e.g., Chatbot), use the raw input
                user_message = chat_input

    # --- Main Processing Block ---
    # This block runs only if a valid user_message was generated from either path
    if user_message:
        try:
            # Efficient: LLM is initialized only once, right when needed
            obj_llm_config = GroqLLM(user_contols_input=user_input)
            model = obj_llm_config.get_llm_model()

            if not model:
                st.error("Error: LLM model could not be initialized.")
                return

            # Build the appropriate graph and run the request
            graph_builder = GraphBuilder(model)
            graph = graph_builder.setup_graph(detected_usecase)
            DisplayResultStreamlit(detected_usecase, graph, user_message).display_result_on_ui()
            
            # Reset the button state after processing is complete
            if st.session_state.get('IsFetchButtonClicked', False):
                st.session_state.IsFetchButtonClicked = False
        
        except Exception as e:
            st.error(f"An application error occurred: {e}")

if __name__ == "__main__":
    load_langgraph_agenticai_app()