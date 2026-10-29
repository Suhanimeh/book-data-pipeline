#  Student Name: Suhani Mehta
#  Student ID: ET21BTAI042
#  Course: Web Programming
#  Academic Year: Third Year B.Tech (AI & DS)
#  Semester: 6
#  Group: 15

from datetime import timedelta

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import PipelineRun, utcnow
from ..pipeline.run import run_pipeline
from ..schemas import RunOut

router = APIRouter(prefix="/api/pipeline", tags=["pipeline"])

STALE_AFTER = timedelta(minutes=30)  # a "running" row older than this is treated as crashed


@router.post("/run", response_model=RunOut, status_code=202)
def trigger_run(background: BackgroundTasks, db: Session = Depends(get_db)):
    active = db.scalar(
        select(PipelineRun)
        .where(PipelineRun.status == "running", PipelineRun.started_at > utcnow() - STALE_AFTER)
    )
    if active:
        raise HTTPException(status_code=409, detail="A pipeline run is already in progress")

    run = PipelineRun(status="running")
    db.add(run)
    db.commit()
    background.add_task(run_pipeline, run.id)
    return run


@router.get("/runs", response_model=list[RunOut])
def list_runs(limit: int = 10, db: Session = Depends(get_db)):
    return db.scalars(select(PipelineRun).order_by(PipelineRun.id.desc()).limit(min(limit, 50))).all()
