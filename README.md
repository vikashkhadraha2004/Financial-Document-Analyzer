# 💹 Financial Document Analyzer

A robust, AI-powered system designed to analyze corporate financial reports, investment updates, and financial statements. This project leverages **CrewAI** for multi-agent orchestration and **FastAPI** for a sleek backend interface, providing automated, professional insights for investors and analysts.

---

## 🛠️ Setup & Installation

Follow these steps to get the project running on your local machine.

### 1. Prerequisites
*   **Python 3.12** (Highly recommended for stability with AI libraries).
*   API keys for **Google Gemini** and **Serper**.

### 2. Environment Configuration
Create a `.env` file in the root directory and add your API keys:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### 3. Installation
Create a virtual environment and install the required dependencies:
```bash
# Create virtual environment
python -3.12 -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4. Running the Server (Sync/Async)
*See the Worker Model section below for the concurrent/asynchronous version.*

---

## 🏗️ Worker Model (Concurrent Processing)

The system is now upgraded to a **Queue Worker Model** to handle concurrent requests efficiently. Instead of waiting for the AI to finish in the HTTP request, the task is offloaded to a **Celery** worker.

### Prerequisites for Worker Mode
*   **Redis Server**: Required as the message broker.
    *   *Windows*: Use [Redis-Windows](https://github.com/tporadowski/redis/releases) or WSL.
    *   *Linux/Docker*: `docker run -d -p 6379:6379 redis`

### Starting the System
You now need to run two separate processes:

1.  **Start the Worker**:
    ```bash
    celery -A celery_worker worker --loglevel=info -P solo
    ```
    *(Note: `-P solo` is used for Windows compatibility)*

2.  **Start the API**:
    ```bash
    python main.py
    ```

---

## 🚀 API Documentation (Worker Mode)

### 1. Analyze Document (Async)
Uploads a PDF and returns a `task_id` immediately.
*   **Endpoint**: `POST /analyze`
*   **Response**:
    ```json
    {
      "status": "queued",
      "task_id": "550e8400-e29b-41d4-a716-446655440000",
      "message": "..."
    }
    ```

### 2. Check Status
Retrieve the result using the `task_id`.
*   **Endpoint**: `GET /status/{task_id}`
*   **Response**:
    ```json
    {
      "task_id": "...",
      "status": "SUCCESS",
      "result": "Full AI analysis content here..."
    }
    ```

---

## 🐛 Bugs Found & Fixed


This project was originally a "Debug Assignment" filled with intentional errors. Below is a summary of the key fixes applied:

### Deterministic Bugs
| File | Issue | Fix |
| :--- | :--- | :--- |
| `agents.py` | `llm = llm` self-assignment. | Correctly initialized `ChatGoogleGenerativeAI` with Gemini. |
| `agents.py` | `tool=[...]` singular attribute. | Changed to `tools=[...]` as required by CrewAI. |
| `tools.py` | `Pdf` class undefined. | Replaced with `PyPDFLoader` from `langchain_community`. |
| `task.py` | Incomplete agent/tool imports. | Properly imported and linked all agents and their respective tools. |
| `main.py` | Incomplete Crew setup. | Rewrote `run_crew` to include all 4 specialized agents and tasks. |
| `requirements.txt` | Missing dependencies. | Added `pypdf`, `langchain-google-genai`, `uvicorn`, and `python-multipart`. |

### Inefficient Prompts
*   **Agent Personas**: Overhauled the `role`, `goal`, and `backstory` for all agents. Removed instructions to "make up facts" and replaced them with professional, data-driven personas.
*   **Task Specificity**: Updated task descriptions to explicitly use the `read_financial_document` tool and focus on providing structured, ethical investment advice.
*   **Output Control**: Changed `expected_output` fields to require professional reports and strategic advisory notes instead of jargon-heavy or contradictory text.

---

## 🚀 API Documentation

### 1. Health Check
Checks if the API is up and running.
*   **Endpoint**: `GET /`
*   **Response**:
    ```json
    { "message": "Financial Document Analyzer API is running" }
    ```

### 2. Analyze Document
Uploads a PDF and returns a comprehensive financial analysis.
*   **Endpoint**: `POST /analyze`
*   **Parameters**:
    *   `file`: The PDF document to analyze.
    *   `query` (Optional): A custom query for the analysis (Default: "Analyze this financial document for investment insights").
*   **Response**:
    ```json
    {
      "status": "success",
      "query": "...",
      "analysis": "...",
      "file_processed": "report.pdf"
    }
    ```

---

## 👥 Meet the Crew
*   **Financial Compliance Verifier**: Ensures the uploaded document is a valid financial report.
*   **Senior Financial Analyst**: Extracts key metrics and identifies market trends.
*   **Investment Strategy Advisor**: Translates analysis into actionable recommendations (Buy/Hold/Sell).
*   **Risk Management Specialist**: Identifies potential internal and external risk factors.

---

## 📝 License
This project is for educational purposes. Always perform your own research before making financial decisions.
