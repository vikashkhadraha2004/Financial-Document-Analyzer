## Importing libraries and files
from crewai import Task

from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from tools import search_tool, read_data_tool, analyze_investment_tool, create_risk_assessment_tool

## Creating a task to help solve user's query
analyze_financial_document = Task(
    description="Analyze the financial document at {file_path} in the context of the user's query: {query}. "
                "Use the read_financial_document tool to extract data from the PDF. "
                "Identify key financial metrics, performance indicators, and any significant trends mentioned in the report. "
                "If necessary, search the internet for additional context on the company or market conditions.",

    expected_output="A comprehensive financial analysis report including key findings, financial health indicators, "
                    "and relevant market comparisons. The report should be professional and data-driven.",

    agent=financial_analyst,
    tools=[read_data_tool, search_tool],
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    description="Based on the financial analysis provided for the document at {file_path}, develop investment recommendations. "
                "Consider the company's financial strength, growth prospects, and potential valuation. "
                "Use the analyze_investment tool to formalize insights and provide a clear recommendation (Buy/Hold/Sell) "
                "if appropriate based on the data.",

    expected_output="A strategic investment advisory note detailing specific recommendations, rationale for those "
                    "recommendations, and potential target price or valuation ranges if data permits.",

    agent=investment_advisor,
    tools=[analyze_investment_tool, search_tool],
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    description="Evaluate the potential risks associated with the financial data at {file_path} and the developed investment strategy. "
                "Identify internal company risks (e.g., debt levels, operational issues) and external market risks "
                "(e.g., regulatory changes, competitive landscape). Use the create_risk_assessment tool "
                "to structure your findings.",

    expected_output="A detailed risk assessment report highlighting primary risk factors, their potential impact, "
                    "and suggested mitigation strategies where applicable.",

    agent=risk_assessor,
    tools=[create_risk_assessment_tool],
    async_execution=False,
)

    
verification = Task(
    description="Verify the document at {file_path} to ensure it is a valid and relevant financial report for analysis. "
                "Confirm that the document contains data necessary for the subsequent financial and investment analysis tasks.",


    expected_output="A verification statement confirming the document's validity and relevance, or flagging issues if the document is unsuitable.",

    agent=verifier,
    tools=[],
    async_execution=False
)