from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from sqlalchemy.orm import Session
import os
import uuid

# Models and DB
from database import SessionLocal, AnalysisTaskDB

# Celery
from celery_worker import process_financial_document

app = FastAPI(title="Financial Document Analyzer")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_endpoint(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
    db: Session = Depends(get_db)
):
    """Queue financial document analysis via Celery Background Worker"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query == "" or query is None:
            query = "Analyze this financial document for investment insights"
            
        # Create Database Record
        db_task = AnalysisTaskDB(
            id=file_id,
            status="PROCESSING",
            file_name=file.filename,
            query=query.strip(),
            analysis_result=None
        )
        db.add(db_task)
        db.commit()

        # Submit task to Celery
        try:
            process_financial_document.delay(file_id, file_path, query.strip())
        except Exception as e:
            # If celery fails to queue, fallback might be needed but we raise 500
            db_task.status = "FAILED"
            db_task.analysis_result = f"Error queueing task to Celery: {str(e)}"
            db.commit()
            raise Exception("Celery is not running or Redis is unaccessible.")
        
        return {
            "task_id": file_id,
            "status": "PROCESSING",
            "message": "Task successfully queued. Use /tasks/{task_id} to check the status."
        }
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")

@app.get("/tasks/{task_id}")
async def get_task_status(task_id: str, db: Session = Depends(get_db)):
    """Retrieve the status and specific result of an analysis task"""
    task = db.query(AnalysisTaskDB).filter(AnalysisTaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task ID not found")
        
    return {
        "task_id": task.id,
        "status": task.status,
        "file_name": task.file_name,
        "query": task.query,
        "analysis_result": task.analysis_result
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)