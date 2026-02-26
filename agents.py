## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import search_tool, read_data_tool, analyze_investment_tool, create_risk_assessment_tool

### Loading LLM
# Fix: Correctly initialize the LLM using ChatGoogleGenerativeAI
# Assuming GOOGLE_API_KEY is in environment variables
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.2,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Creating an Experienced Financial Analyst agent
financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Provide accurate and insightful financial analysis based on provided documents for query: {query}",
    verbose=True,
    memory=True,
    backstory=(
        "You are a seasoned financial analyst with decades of experience in equity research and corporate finance. "
        "You excel at identifying key financial trends, analyzing balance sheets, and extracting meaningful insights "
        "from complex financial reports. Your analysis is objective, data-driven, and focused on providing value."
    ),
    tools=[read_data_tool, search_tool], # Fix: Use 'tools' instead of 'tool'
    llm=llm,
    max_iter=10, # Fix: Increase from 1 to allow reasoning
    max_rpm=10,
    allow_delegation=True
)

# Creating a document verifier agent
verifier = Agent(
    role="Financial Compliance & Document Verifier",
    goal="Verify the authenticity and relevance of financial documents provided.",
    verbose=True,
    memory=True,
    backstory=(
        "You have a background in financial audit and compliance. Your primary role is to ensure that the "
        "documents being analyzed are indeed relevant financial reports and to flag any inconsistencies "
        "or missing information that might impact the analysis."
    ),
    llm=llm,
    max_iter=5,
    max_rpm=10,
    allow_delegation=True
)


investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal="Develop sound investment recommendations based on financial analysis and market context.",
    verbose=True,
    backstory=(
        "You are an expert in portfolio management and investment strategy. You take the analysis provided by "
        "the financial analyst and translate it into actionable investment advice, considering current market "
        "conditions and potential long-term growth opportunities."
    ),
    tools=[analyze_investment_tool, search_tool],
    llm=llm,
    max_iter=10,
    max_rpm=10,
    allow_delegation=False
)


risk_assessor = Agent(
    role="Risk Management Specialist",
    goal="Identify and quantify potential risks associated with the financial data and investment strategies.",
    verbose=True,
    backstory=(
        "You specialize in identifying financial, operational, and market risks. You look beyond the numbers "
        "to see potential pitfalls, macro-economic threats, and internal vulnerabilities that could affect "
        "financial stability or investment performance."
    ),
    tools=[create_risk_assessment_tool],
    llm=llm,
    max_iter=10,
    max_rpm=10,
    allow_delegation=False
)

