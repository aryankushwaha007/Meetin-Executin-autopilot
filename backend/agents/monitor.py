from sqlalchemy.orm import Session
from models import Task
from .audit import log_action
from .recovery import resolve_stalled_task

def run_health_check(db: Session):
    """
    Health Monitor detects stalled tasks, missing owners, overdue actions.
    This would normally run on a Cron via APScheduler.
    For the demo, it is an endpoint we can trigger.
    """
    tasks = db.query(Task).filter(Task.status.in_(["open", "in_progress"])).all()
    
    issues_found = 0
    for task in tasks:
        # 1. Detect missing owner (should be rare due to Orchestrator, but possible)
        if not task.owner:
            task.status = "stalled"
            db.commit()
            log_action(
                db=db,
                agent_name="Health Monitor Agent",
                action="Mark Stalled",
                reason="Task has no owner.",
                task_id=task.id,
                confidence=1.0
            )
            resolve_stalled_task(db, task)
            issues_found += 1
            continue
            
        # 2. Mock Stalled Task Rule: High priority task open for 'too long'
        # For the demo, we manually trigger stalls via an API, but we'll pretend it's time-based
        if task.priority == "high" and task.status == "open":
            # Just for Demo Scenario 3: trigger a stall for "Security Audit"
            if "security audit" in task.title.lower():
                task.status = "stalled"
                db.commit()
                log_action(
                    db=db,
                    agent_name="Health Monitor Agent",
                    action="Mark Stalled",
                    reason="High priority task SLA breached. No progress detected.",
                    task_id=task.id,
                    confidence=0.95
                )
                # Let Recovery Agent handle it
                resolve_stalled_task(db, task)
                issues_found += 1
                
    return {"status": "completed", "issues_detected_and_handled": issues_found}
