"""
Symphony AI - Main FastAPI Application
"""
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import shutil
from pathlib import Path
from datetime import datetime
import uuid

from .core.config import settings
from .models import init_db, get_db, AnalysisJob
from .schemas import JobStatus, AnalysisResults
from .services.orchestrator import AnalysisOrchestrator

# Initialize FastAPI app
app = FastAPI(
    title="Symphony AI",
    description="Multi-modal Financial Analysis Platform",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = AnalysisOrchestrator()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("🎵 Symphony AI started successfully!")
    print(f"📊 Database initialized at {settings.DATABASE_URL}")
    print(f"📁 Upload directory: {settings.UPLOAD_DIR}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Symphony AI - Multi-modal Financial Analysis Platform",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "anthropic_configured": bool(settings.ANTHROPIC_API_KEY),
        "openai_configured": bool(settings.OPENAI_API_KEY),
    }


@app.post("/api/analyze", response_model=JobStatus)
async def analyze_earnings_call(
    audio: UploadFile = File(..., description="Earnings call audio file (mp3, wav, m4a)"),
    charts: Optional[List[UploadFile]] = File(None, description="Financial chart images (optional)"),
    company_name: Optional[str] = Form(None),
    company_context: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Main analysis endpoint - Upload audio and optional charts for analysis
    """
    try:
        # Validate audio file
        if not audio.filename:
            raise HTTPException(status_code=400, detail="No audio file provided")

        # Check file extension
        allowed_audio_extensions = {".mp3", ".wav", ".m4a", ".flac", ".ogg"}
        audio_ext = Path(audio.filename).suffix.lower()
        if audio_ext not in allowed_audio_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid audio format. Allowed: {', '.join(allowed_audio_extensions)}"
            )

        # Generate job ID first
        job_id = str(uuid.uuid4())

        # Save audio file BEFORE creating job
        audio_path = settings.AUDIO_DIR / f"{job_id}_{audio.filename}"
        with open(audio_path, "wb") as buffer:
            shutil.copyfileobj(audio.file, buffer)

        # Save chart files if provided
        chart_paths = []
        if charts:
            for i, chart in enumerate(charts):
                if chart.filename:
                    chart_ext = Path(chart.filename).suffix.lower()
                    if chart_ext not in {".png", ".jpg", ".jpeg", ".pdf"}:
                        continue
                    chart_path = settings.CHARTS_DIR / f"{job_id}_chart_{i}{chart_ext}"
                    with open(chart_path, "wb") as buffer:
                        shutil.copyfileobj(chart.file, buffer)
                    chart_paths.append(str(chart_path))

        # Create analysis job WITH audio_path already set
        job = AnalysisJob(
            id=job_id,
            company_name=company_name,
            company_context=company_context,
            audio_path=str(audio_path),
            chart_paths=chart_paths,
            status="pending",
        )
        db.add(job)
        db.commit()
        db.refresh(job)

        # Start processing asynchronously (in background for demo purposes)
        # In production, this would use Celery or similar task queue
        import threading
        thread = threading.Thread(
            target=orchestrator.process_job,
            args=(job.id,)
        )
        thread.start()

        return JobStatus(
            id=job.id,
            status=job.status,
            progress=job.progress,
            created_at=job.created_at.isoformat() if job.created_at else None,
        )

    except Exception as e:
        print(f"❌ Error in /api/analyze: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/status/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Get processing status of an analysis job
    """
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatus(
        id=job.id,
        status=job.status,
        progress=job.progress,
        error_message=job.error_message,
        created_at=job.created_at.isoformat() if job.created_at else None,
        started_at=job.started_at.isoformat() if job.started_at else None,
        completed_at=job.completed_at.isoformat() if job.completed_at else None,
    )


@app.get("/api/results/{job_id}")
async def get_analysis_results(job_id: str, db: Session = Depends(get_db)):
    """
    Retrieve complete analysis results
    """
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if job.status != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job is not completed yet. Current status: {job.status}"
        )

    return job.get_full_results()


@app.get("/api/jobs")
async def list_jobs(
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    List all analysis jobs
    """
    jobs = db.query(AnalysisJob)\
        .order_by(AnalysisJob.created_at.desc())\
        .offset(offset)\
        .limit(limit)\
        .all()

    total = db.query(AnalysisJob).count()

    return {
        "jobs": [job.to_dict() for job in jobs],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@app.delete("/api/jobs/{job_id}")
async def delete_job(job_id: str, db: Session = Depends(get_db)):
    """
    Delete an analysis job and its associated files
    """
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Delete associated files
    try:
        if job.audio_path and Path(job.audio_path).exists():
            Path(job.audio_path).unlink()

        if job.chart_paths:
            for chart_path in job.chart_paths:
                if Path(chart_path).exists():
                    Path(chart_path).unlink()
    except Exception as e:
        print(f"Error deleting files: {e}")

    # Delete from database
    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully", "job_id": job_id}


@app.get("/api/audio/{job_id}")
async def get_audio_file(job_id: str, db: Session = Depends(get_db)):
    """
    Serve audio file for a job
    """
    job = db.query(AnalysisJob).filter(AnalysisJob.id == job_id).first()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    if not job.audio_path or not Path(job.audio_path).exists():
        raise HTTPException(status_code=404, detail="Audio file not found")

    return FileResponse(
        job.audio_path,
        media_type="audio/mpeg",
        filename=Path(job.audio_path).name
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
