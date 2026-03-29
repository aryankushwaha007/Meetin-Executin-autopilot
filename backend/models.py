from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text, Float
from sqlalchemy.orm import relationship
import datetime

from database import Base

class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    transcript = Column(Text)
    status = Column(String, default="pending") # processing, completed, failed
    
    tasks = relationship("Task", back_populates="meeting")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(Integer, ForeignKey("meetings.id"))
    title = Column(String)
    description = Column(Text, nullable=True)
    owner = Column(String, nullable=True)
    deadline = Column(DateTime, nullable=True)
    priority = Column(String, default="medium")
    dependencies = Column(String, nullable=True)
    status = Column(String, default="open") # open, in_progress, stalled, escalated, completed
    risk_level = Column(String, default="low") # low, medium, high
    
    meeting = relationship("Meeting", back_populates="tasks")
    logs = relationship("AuditLog", back_populates="task")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    agent_name = Column(String) # Extractor, Orchestrator, Assignee, Monitor, Recovery
    action = Column(String)
    reason = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    confidence_score = Column(Float, nullable=True)
    human_approval_required = Column(Boolean, default=False)
    
    task = relationship("Task", back_populates="logs")
