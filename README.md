# Financial Document Analyzer

A comprehensive AI-powered financial document analysis system that processes corporate reports, financial statements, and investment documents using AI agents (CrewAI).

## Project Overview
This project takes uploaded financial documents (PDFs) and uses a pipeline of specialized AI agents (Verifier, Financial Analyst, Investment Advisor, Risk Assessor) to extract, analyze, and map complex metrics into actionable investment advice and a comprehensive risk assessment. 

## Bugs Found & Fixes Implemented
During the debugging phase, several deterministic bugs and inefficient prompts were addressed:
1. **Uvicorn Reload Error (`main.py`)**: Fixed the `uvicorn.run()` import string to `"main:app"` to allow hot-reloading.
2. **Variable Shadowing (`main.py`)**: The `/analyze` endpoint function shadowed the `analyze_financial_document` crew task, breaking the sequence. Renamed to `analyze_endpoint`.
3. **Crew Initialization (`main.py`)**: The pipeline skipped the Verifier, Investment Advisor, and Risk Assessor. Re-wired `run_crew()` to correctly execute all four agents sequentially and pass `file_path`.
4. **Unprofessional Hallucinations (`agents.py` & `task.py`)**: The agents' roles, goals, and backstories contained satirical prompt instructions to hallucinate and invent data. These were entirely rewritten to provide factual, professional, and context-aware financial analysis.
5. **Broken Tools (`tools.py`)**: Removed placeholder `InvestmentTool` and `RiskTool` which had infinite loops and syntax errors. Encapsulated and secured `FinancialDocumentTool` with standard BaseTool structures and safe parsing logic.

## Setup and Usage Instructions

### Prerequisites
- Python 3.10+
- OpenAI API Key (or configured LLM in `.env`)
- Redis server (for the Celery Message Queue)

### Installation
1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows: venv\Scripts\activate
   # On Unix/MacOS: source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   pip install sqlalchemy celery redis
   ```
4. Create a `.env` file in the root directory and add your keys:
   ```env
   OPENAI_API_KEY=your_key_here
   ```

### Running the Application

This application uses a Queue Worker model via Celery to handle background processing. You need to run the API server and the Celery worker concurrently.

1. **Start the Redis Server:** Ensure your local Redis server is running (default `redis://localhost:6379/0`).
2. **Start the Database:** The SQLite database will be auto-generated upon the first request.
3. **Start the Celery Worker**:
   ```bash
   celery -A worker.celery worker --loglevel=info -P gevent # (or solo for Windows)
   ```
4. **Start the FastAPI Application**:
   ```bash
   python main.py
   ```

## API Documentation

### 1. Health Check
- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns the operational status of the API.
- **Response**: `{"message": "Financial Document Analyzer API is running"}`

### 2. Analyze Document
- **URL**: `/analyze`
- **Method**: `POST`
- **Description**: Upload a PDF financial document. The document will be queued for background analysis via Celery.
- **Parameters**: 
  - `file`: (FormData) The PDF file to be analyzed.
  - `query`: (FormData) Optional context or question regarding the financials.
- **Response**: 
  ```json
  {
    "task_id": "string (UUID)",
    "status": "Processing"
  }
  ```

### 3. Get Analysis Result
- **URL**: `/tasks/{task_id}`
- **Method**: `GET`
- **Description**: Fetch the status and result of the previously queued task from the database.
- **Response**:
  ```json
  {
    "task_id": "string",
    "status": "PROCESSING | COMPLETED | FAILED",
    "file_name": "string",
    "query": "string",
    "analysis_result": "string (or null)"
  }
  ```
