import os
from celery import Celery
from dotenv import load_dotenv
load_dotenv()

# Configure Celery
# CELERY_BROKER_URL is usually redis://localhost:6379/0
broker_url = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

celery_app = Celery("financial_worker", broker=broker_url, backend=result_backend)

# To import the crew logic independently
from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment, verification

@celery_app.task(name="process_financial_analysis")
def process_financial_analysis(query, file_path):
    """
    Worker task to run the CrewAI orchestration as a background process.
    """
    try:
        financial_crew = Crew(
            agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
            tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
            process=Process.sequential,
        )
        
        # CrewAI kickoff for background processing
        result = financial_crew.kickoff({'query': query, 'file_path': file_path})
        
        # Returns the result to Celery's backend
        return {
            "status": "completed",
            "result": str(result)
        }
        
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }
