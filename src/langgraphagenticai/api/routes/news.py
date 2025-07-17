# src/langgraphagenticai/api/routes/news.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
from src.langgraphagenticai.api.schemas.models import NewsInvokeRequest, NewsRequest, NewsResponse
from src.langgraphagenticai.api.core.dependencies import initialize_llm, check_tool_keys, check_email_credentials
from src.langgraphagenticai.graph.graph_builder import GraphBuilder
from src.langgraphagenticai.utils.message_parser import NewsMessageParser
from src.langgraphagenticai.tools.translation_tool import SUPPORTED_LANGUAGES

router = APIRouter()

def _run_news_graph_and_get_path(llm, frequency: str, topic: str, language: str, recipient_email: str | None) -> str:
    """Helper function to build and run the news graph, returning the output file path."""
    user_message = f"{frequency}:{topic}:{language}:{recipient_email or ''}"
    graph = GraphBuilder(llm).setup_graph("News")
    final_state = graph.invoke({"messages": [("user", user_message)]})
    md_path = final_state.get('md_filename')
    if not md_path or not os.path.exists(md_path):
        raise HTTPException(status_code=500, detail="News agent failed to generate the summary file.")
    return md_path

@router.post("/invoke", response_model=NewsResponse, summary="Invoke News Agent with Query")
async def invoke_news_agent(request: NewsInvokeRequest):
    check_tool_keys()
    check_email_credentials(request.recipient_email)
    
    parser = NewsMessageParser()
    if not parser.is_news_request(request.query):
        raise HTTPException(status_code=400, detail="The provided query does not seem to be a news request.")
    
    parsed = parser.parse_news_message(request.query)
    llm = initialize_llm(request.model)

    md_path = _run_news_graph_and_get_path(llm, parsed['frequency'], parsed['topic'], parsed['language'], request.recipient_email)
    
    return NewsResponse(success=True, message=f"News processing initiated.", filename=os.path.basename(md_path), file_path=md_path, processing_details=parsed)

@router.post("/structured", response_model=NewsResponse, summary="Fetch News with Structured Data")
async def fetch_news_structured(request: NewsRequest):
    check_tool_keys()
    check_email_credentials(request.recipient_email)
    
    if request.language not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {request.language}")
        
    llm = initialize_llm(request.model)
    
    md_path = _run_news_graph_and_get_path(llm, request.frequency.lower(), request.topic, request.language, request.recipient_email)
    
    return NewsResponse(success=True, message="News processed successfully.", filename=os.path.basename(md_path), file_path=md_path, processing_details=request.dict())

@router.get("/download/{filename}", summary="Download News File")
async def download_file(filename: str):
    file_path_pdf = f"./News/{filename.replace('.md', '.pdf')}"
    if os.path.exists(file_path_pdf):
        return FileResponse(path=file_path_pdf, filename=os.path.basename(file_path_pdf), media_type='application/pdf')
    
    file_path_md = f"./News/{filename}"
    if os.path.exists(file_path_md):
        return FileResponse(path=file_path_md, filename=filename, media_type='text/markdown')

    raise HTTPException(status_code=404, detail="File not found.")

@router.get("/files", summary="List News Files")
async def list_news_files():
    news_dir = "./News"
    if not os.path.exists(news_dir):
        return {"files": []}
    files = [{"filename": f, "size_bytes": os.path.getsize(os.path.join(news_dir, f))} for f in os.listdir(news_dir) if f.endswith(('.md', '.pdf'))]
    return {"files": files, "count": len(files)}

@router.delete("/files/{filename}", summary="Delete News File")
async def delete_news_file(filename: str):
    file_path = f"./News/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")
    try:
        os.remove(file_path)
        return {"success": True, "message": f"File '{filename}' deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")