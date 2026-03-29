from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas
from agents.extractor import extract_tasks_from_transcript
from agents.orchestrator import create_tasks_from_extracted_data
from agents.audit import log_action

router = APIRouter(prefix="/meetings", tags=["Meetings"])

@router.get("/", response_model=List[schemas.Meeting])
def get_meetings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Meeting).offset(skip).limit(limit).all()

@router.post("/", response_model=schemas.Meeting)
def create_meeting(meeting: schemas.MeetingCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_meeting = models.Meeting(title=meeting.title, transcript=meeting.transcript, status="processing")
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    
    # Process transcript in background
    background_tasks.add_task(process_meeting_transcript, db_meeting.id, db)
    
    return db_meeting

def process_meeting_transcript(meeting_id: int, db: Session):
    meeting = db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()
    if not meeting:
        return
        
    try:
        # Step 1: Extractor Agent
        extracted_data = extract_tasks_from_transcript(meeting.transcript)
        
        log_action(
            db=db,
            agent_name="Extractor Agent",
            action="Extract Decisions",
            reason=f"Found {len(extracted_data)} actionable items in transcript.",
            confidence=0.9
        )
        
        # Step 2: Orchestrator Agent
        create_tasks_from_extracted_data(db, meeting_id, extracted_data)
        
        meeting.status = "completed"
        db.commit()
        
    except Exception as e:
        meeting.status = "failed"
        db.commit()
        print(f"Extraction failed: {str(e)}")
