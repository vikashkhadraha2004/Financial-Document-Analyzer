from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment, verification

from celery_worker import process_financial_analysis, celery_app
from celery.result import AsyncResult

app = FastAPI(title="Financial Document Analyzer (Queued)")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running in Worker Mode"}

@app.post("/analyze")
async def analyze_financial_document_async(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """
    Queue analysis as a background task and return a task ID immediately.
    This handles concurrency by offloading the intensive AI processing to Workers.
    """
    file_id = str(uuid.uuid4())
    # Keep file permanently for worker access in a real scenario, but for demo we store in data/ 
    # NOTE: Workers must share the filesystem (like local dev) or use S3 in production.
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if not query:
            query = "Analyze this financial document for investment insights"

        # Dispatch task to Celery
        task = process_financial_analysis.delay(query=query.strip(), file_path=file_path)
        
        return {
            "status": "queued",
            "task_id": task.id,
            "message": "The financial analysis has been queued. Use /status/{task_id} to get results.",
            "file_name": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error queueing analysis: {str(e)}")

@app.get("/status/{task_id}")
async def get_task_status(task_id: str):
    """
    Check the status of a specific analysis task.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    
    response = {
        "task_id": task_id,
        "status": task_result.status, # PENDING, STARTED, SUCCESS, FAILURE
    }

    if task_result.ready():
        result = task_result.result
        if isinstance(result, dict) and "error" in result:
             response["status"] = "FAILURE"
             response["error"] = result["error"]
        else:
             response["result"] = result.get("result") if isinstance(result, dict) else result

    return response

# Standard Sync Version for quick tests
@app.post("/analyze/sync")
async def analyze_sync_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Legacy synchronous endpoint for small docs/debugging."""
    # (Existing run_crew logic)
    from main_v1 import run_crew # assuming we keep the old logic or re-import
    # ... logic here ...
    pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)