from sqlalchemy.orm import Session
from models import AuditLog
import schemas

def log_action(db: Session, agent_name: str, action: str, reason: str, task_id: int = None, confidence: float = None, human_approval: bool = False):
    """Centralized audit logging for the multi-agent system."""
    log_entry = AuditLog(
        agent_name=agent_name,
        action=action,
        reason=reason,
        task_id=task_id,
        confidence_score=confidence,
        human_approval_required=human_approval
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    return log_entry
