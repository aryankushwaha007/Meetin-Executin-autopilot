from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from database import get_db
import models
import schemas
from agents.monitor import run_health_check
from agents.audit import log_action
from agents.verification import verify_completed_task

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/at-risk")
def get_at_risk_tasks(db: Session = Depends(get_db)):
    """
    Bottleneck Prediction endpoint.
    Returns tasks predicted to breach SLA based on risk signals.
    Signals: high priority + open status. In production this would use time-based SLA windows.
    """
    all_open = db.query(models.Task).filter(models.Task.status.in_(["open", "in_progress"])).all()
    
    at_risk = []
    for task in all_open:
        risk_score = 0
        reasons = []
        
        if task.priority == "high":
            risk_score += 40
            reasons.append("High priority")
        if task.risk_level == "high":
            risk_score += 35
            reasons.append("High risk classification")
        if not task.owner:
            risk_score += 25
            reasons.append("No owner assigned")
        if task.dependencies:
            risk_score += 15
            reasons.append("Has unresolved dependencies")
            
        if risk_score >= 40:
            at_risk.append({
                "id": task.id,
                "title": task.title,
                "owner": task.owner,
                "priority": task.priority,
                "risk_level": task.risk_level,
                "status": task.status,
                "risk_score": min(risk_score, 99),
                "breach_predicted_in": f"{max(1, 48 - risk_score // 2)}h",
                "signals": reasons
            })
    
    # Sort by highest risk first
    at_risk.sort(key=lambda x: x["risk_score"], reverse=True)
    return at_risk

@router.get("/", response_model=List[schemas.Task])
def get_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Task).offset(skip).limit(limit).all()

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/trigger-health-monitor")
def trigger_health_monitor(db: Session = Depends(get_db)):
    """Manually triggers the health monitor for the demo."""
    result = run_health_check(db)
    return result

@router.put("/{task_id}/status")
def update_task_status(task_id: int, status: str, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    valid_statuses = ["open", "in_progress", "stalled", "escalated", "completed", "cancelled"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")

    old_status = task.status
    task.status = status
    db.commit()
    
    log_action(
        db=db,
        agent_name="Human Operator",
        action=f"Status Update: {old_status} → {status}",
        reason=f"Manual status change applied via dashboard.",
        task_id=task.id,
        confidence=1.0
    )

    # Trigger Verification Agent when a task is marked complete
    if status == "completed":
        verify_completed_task(db, task)
    
    return task
