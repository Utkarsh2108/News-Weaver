# src/langgraphagenticai/api/routes/chat.py

from fastapi import APIRouter, HTTPException
import json
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from src.langgraphagenticai.api.schemas.models import ChatRequest, WebChatRequest, ChatResponse, WebChatResponse
from src.langgraphagenticai.api.core.dependencies import initialize_llm, check_tool_keys
from src.langgraphagenticai.graph.graph_builder import GraphBuilder

router = APIRouter()

@router.post("/basic", response_model=ChatResponse, summary="Basic Chatbot")
async def basic_chatbot(request: ChatRequest):
    llm = initialize_llm(request.model if hasattr(request, 'model') else "llama3-8b-8192") # Handle model attribute for basic request
    graph = GraphBuilder(llm).setup_graph("Basic Chatbot")
    try:
        response = graph.invoke({'messages': [("user", request.message)]})
        ai_message = response['messages'][-1].content
        return ChatResponse(success=True, response=ai_message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chatbot processing failed: {str(e)}")

@router.post("/web", response_model=WebChatResponse, summary="Web-Enabled Chatbot")
async def web_chatbot(request: WebChatRequest):
    check_tool_keys()
    llm = initialize_llm(request.model)
    graph = GraphBuilder(llm).setup_graph("Chatbot With Web")
    try:
        initial_state = {"messages": [HumanMessage(content=request.message)]}
        final_response = graph.invoke(initial_state)
        
        ai_message = ""
        tool_outputs = [json.loads(msg.content) for msg in final_response['messages'] if isinstance(msg, ToolMessage)]
        for msg in final_response['messages']:
            if isinstance(msg, AIMessage) and msg.content:
                ai_message = msg.content
                break

        if not ai_message:
            raise HTTPException(status_code=500, detail="Failed to get a final response from the AI.")
            
        return WebChatResponse(success=True, response=ai_message, tool_outputs=tool_outputs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Web Chatbot processing failed: {str(e)}")