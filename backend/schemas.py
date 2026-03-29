from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    owner: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[str] = "medium"
    dependencies: Optional[str] = None
    risk_level: Optional[str] = "low"

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    meeting_id: int
    status: str

    class Config:
        from_attributes = True

class MeetingBase(BaseModel):
    title: str
    transcript: str

class MeetingCreate(MeetingBase):
    pass

class Meeting(MeetingBase):
    id: int
    date: datetime
    status: str
    tasks: List[Task] = []

    class Config:
        from_attributes = True

class AuditLogCreate(BaseModel):
    agent_name: str
    action: str
    reason: str
    confidence_score: Optional[float] = None
    human_approval_required: Optional[bool] = False

class AuditLog(AuditLogCreate):
    id: int
    task_id: Optional[int] = None
    timestamp: datetime
    
    class Config:
        from_attributes = True
