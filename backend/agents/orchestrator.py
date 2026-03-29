from sqlalchemy.orm import Session
from models import Task
from .audit import log_action

def create_tasks_from_extracted_data(db: Session, meeting_id: int, extracted_tasks: list):
    """
    Workflow Orchestrator Agent.
    Takes extracted data and creates structured tasks in the system.
    Returns the created tasks.
    """
    created_tasks = []
    
    for task_data in extracted_tasks:
        # Create the new task
        new_task = Task(
            meeting_id=meeting_id,
            title=task_data["title"],
            description=task_data.get("description"),
            owner=task_data.get("owner"),
            priority=task_data.get("priority", "medium"),
            risk_level=task_data.get("risk_level", "low"),
            dependencies=task_data.get("dependencies"),
            status="pending_approval" if task_data.get("confidence", 1.0) < 0.8 else "open"
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        # Log the Orchestrator's action
        log_action(
            db=db,
            agent_name="Orchestrator Agent",
            action="Create Task",
            reason=f"Extracted from transcript with confidence {task_data.get('confidence', 0.0)}",
            task_id=new_task.id,
            confidence=task_data.get("confidence", 0.0),
            human_approval=task_data.get("confidence", 1.0) < 0.8
        )
        
        # Trigger explicit owner assignment check
        if not new_task.owner:
            _assign_owner_fallback(db, new_task)
            
        created_tasks.append(new_task)
        
    return created_tasks

def _assign_owner_fallback(db: Session, task: Task):
    """Owner Assignment Agent - fallback if missing"""
    # Mock fallback logic
    inferred_owner = "Engineering Lead" if "database" in task.title.lower() else "Product Manager"
    
    task.owner = inferred_owner
    db.commit()
    
    log_action(
        db=db,
        agent_name="Owner Assignment Agent",
        action="Assign Owner",
        reason=f"Owner was missing. Inferred {inferred_owner} based on task context.",
        task_id=task.id,
        confidence=0.7,
        human_approval=True # Requires review because it was guessed
    )
