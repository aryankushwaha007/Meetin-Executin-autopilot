from sqlalchemy.orm import Session
from models import Task
from .audit import log_action

def resolve_stalled_task(db: Session, task: Task):
    """
    Recovery Agent self-corrects by reassigning, rescheduling, or escalating.
    """
    if task.status == "stalled":
        if "security audit" in task.title.lower() or task.risk_level == "high":
            task.status = "escalated"
            task.owner = "VP of Engineering" # Escalation
            db.commit()
            
            log_action(
                db=db,
                agent_name="Escalation Agent",
                action="Escalate Task",
                reason="High risk stalled task automatically escalated to VP of Engineering.",
                task_id=task.id,
                confidence=0.99
            )
        else:
            task.status = "open"
            task.priority = "high"
            db.commit()
            
            log_action(
                db=db,
                agent_name="Recovery Agent",
                action="Bump Priority",
                reason="Stalled low-risk task reprioritized to high.",
                task_id=task.id,
                confidence=0.85
            )
    
    # Mock recovery for Missing Owner (e.g. from human clearing the owner, or fallback failing)
    if not task.owner:
        task.status = "escalated"
        db.commit()
        log_action(
            db=db,
            agent_name="Recovery Agent",
            action="Escalate Missing Owner",
            reason="Could not determine owner. Escalating to management.",
            task_id=task.id,
            confidence=0.9
        )
    
    return task
