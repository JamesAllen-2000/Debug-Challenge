import os
from celery import Celery
from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, verification, investment_analysis, risk_assessment
from database import SessionLocal, AnalysisTaskDB

celery_app = Celery(
    "worker",
    broker="sqla+sqlite:///celery_broker.sqlite",
    backend="db+sqlite:///celery_results.sqlite"
)

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew"""
    financial_crew = Crew(
        agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
        tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
    )
    
    result = financial_crew.kickoff(inputs={'query': query, 'file_path': file_path})
    return str(result)

@celery_app.task
def process_financial_document(task_id: str, file_path: str, query: str):
    db = SessionLocal()
    try:
        # Execute long running CrewAI process
        response = run_crew(query=query, file_path=file_path)
        
        # Record Success
        task_record = db.query(AnalysisTaskDB).filter(AnalysisTaskDB.id == task_id).first()
        if task_record:
            task_record.status = "COMPLETED"
            task_record.analysis_result = response
            db.commit()

    except Exception as e:
        # Record Failure
        task_record = db.query(AnalysisTaskDB).filter(AnalysisTaskDB.id == task_id).first()
        if task_record:
            task_record.status = "FAILED"
            task_record.analysis_result = str(e)
            db.commit()

    finally:
        db.close()
        # Clean up PDF file to save disk space
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception:
                pass
