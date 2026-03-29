from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db, engine
import models
from agents.audit import log_action

router = APIRouter(prefix="/demo", tags=["Demo Scenarios"])

@router.post("/reset")
def reset_database(db: Session = Depends(get_db)):
    """Resets the entire database. For demo purposes only."""
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    return {"status": "ok", "message": "Database reset entirely."}

@router.post("/seed")
def seed_database(db: Session = Depends(get_db)):
    """Populates basic seed dummy data for the application."""
    # Seed Meeting
    m1 = models.Meeting(
        title="Q3 Engineering Planning",
        transcript="We need to perform database migration for new schema by Friday. Sarah will handle it. Also we need a security audit review, but we're not sure who owns that yet.",
        status="completed"
    )
    db.add(m1)
    db.commit()
    db.refresh(m1)
    
    # Let orchestrator parse it dynamically (we could mock it, but let's just create tasks)
    t1 = models.Task(
        meeting_id=m1.id,
        title="Perform database migration for new schema",
        description="The new user profile schema requires a database migration script.",
        owner="Sarah",
        priority="high",
        risk_level="medium",
        status="open"
    )
    t2 = models.Task(
        meeting_id=m1.id,
        title="Conduct Q3 Security Audit",
        description="Review IAM roles and compliance checklist.",
        owner=None, # Missing owner for Demo Scenario 2
        priority="high",
        risk_level="high",
        status="pending_approval"
    )
    db.add_all([t1, t2])
    db.commit()
    db.refresh(t1)
    db.refresh(t2)
    
    log_action(db, "Orchestrator Agent", "Create Task", "Extracted from Q3 Engineering transcript", t1.id, 0.95)
    log_action(db, "Orchestrator Agent", "Create Task", "Extracted from Q3 Engineering transcript", t2.id, 0.75, human_approval=True)
    
    return {"status": "ok", "message": "Seeded 1 meeting and 2 tasks"}
