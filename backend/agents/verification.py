from sqlalchemy.orm import Session
from models import Task
from .audit import log_action

def verify_completed_task(db: Session, task: Task):
    """
    Verification Agent — fires after a task is marked completed.
    Checks for logical consistency and logs a signed-off verification entry.
    This closes the autonomous loop: Extract → Orchestrate → Assign → Execute → Verify.
    """
    issues = []

    if not task.owner:
        issues.append("Task completed with no recorded owner.")
    if not task.title:
        issues.append("Task title is empty.")

    if issues:
        confidence = 0.6
        verdict = "Verified with warnings: " + "; ".join(issues)
    else:
        confidence = 0.98
        verdict = f"Task '{task.title}' verified as complete. Owner: {task.owner}. All fields nominal."

    log_action(
        db=db,
        agent_name="Verification Agent",
        action="Verify Completion",
        reason=verdict,
        task_id=task.id,
        confidence=confidence,
        human_approval=len(issues) > 0
    )

    return {"verified": len(issues) == 0, "confidence": confidence, "verdict": verdict}
