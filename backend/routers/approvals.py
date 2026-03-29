from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
import models
from agents.audit import log_action

router = APIRouter(prefix="/approvals", tags=["Approvals"])

class ResolveRequest(BaseModel):
    decision: str # "approve" or "reject"

@router.get("/pending")
def get_pending_approvals(db: Session = Depends(get_db)):
    """Fetch all tasks currently pending human approval."""
    tasks = db.query(models.Task).filter(models.Task.status == "pending_approval").all()
    
    results = []
    for t in tasks:
        # Find the specific audit log that flagged this for human review
        log = db.query(models.AuditLog).filter(
            models.AuditLog.task_id == t.id, 
            models.AuditLog.human_approval_required == True
        ).order_by(models.AuditLog.timestamp.desc()).first()
        
        results.append({
            "task": t,
            "log": log
        })
    return results

@router.post("/{task_id}/resolve")
def resolve_approval(task_id: int, req: ResolveRequest, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if req.decision == "approve":
        task.status = "open" # Move out of quarantine
        log_action(db, "Human Admin", "Approve AI Decision", f"Authorized system intervention.", task.id, 1.0, False)
    elif req.decision == "reject":
        task.status = "cancelled"
        log_action(db, "Human Admin", "Reject AI Decision", f"Overruled system intervention.", task.id, 1.0, False)
    else:
        raise HTTPException(status_code=400, detail="Invalid decision")
    
    db.commit()
    return {"status": "ok", "task_id": task.id, "new_status": task.status}
