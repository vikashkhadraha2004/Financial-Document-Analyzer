## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import tool
from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

## Creating search tool
search_tool = SerperDevTool()

## Creating custom pdf reader tool
@tool("read_financial_document")
def read_data_tool(path: str = 'data/sample.pdf'):
    """Tool to read data from a pdf file from a path

    Args:
        path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

    Returns:
        str: Full Financial Document file content
    """
    # Fix: Check for file existence and use PyPDFLoader
    if not os.path.exists(path):
        # Try to find any pdf in data directory if sample.pdf is missing
        if path == 'data/sample.pdf':
            data_dir = 'data'
            if os.path.exists(data_dir):
                pdfs = [f for f in os.listdir(data_dir) if f.endswith('.pdf')]
                if pdfs:
                    path = os.path.join(data_dir, pdfs[0])
                else:
                    return f"Error: File {path} not found and no other PDFs in data/."
            else:
                return f"Error: Data directory {data_dir} not found."
        else:
            return f"Error: File {path} not found."

    try:
        loader = PyPDFLoader(path)
        docs = loader.load()
        
        full_report = ""
        for data in docs:
            content = data.page_content
            # Remove extra whitespaces
            import re
            content = re.sub(r'\n\s*\n', '\n', content)
            full_report += content + "\n"
            
        return full_report
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

## Creating Investment Analysis Tool
@tool("analyze_investment")
def analyze_investment_tool(financial_document_data: str):
    """Processes and analyzes the financial document data for investment insights."""
    # Simple cleanup and placeholder for actual logic
    import re
    processed_data = re.sub(r'\s+', ' ', financial_document_data).strip()
    
    # In a real scenario, this would involve complex analysis
    return f"Analysis of provided financial data: {processed_data[:500]}..."

## Creating Risk Assessment Tool
@tool("create_risk_assessment")
def create_risk_assessment_tool(financial_document_data: str):        
    """Identifies potential risks from the financial document data."""
    return f"Risk assessment based on data summary: {financial_document_data[:500]}..."