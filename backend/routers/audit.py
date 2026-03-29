from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/", response_model=List[schemas.AuditLog])
def get_audit_logs(skip: int = 0, limit: int = 100, task_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.AuditLog)
    if task_id:
        query = query.filter(models.AuditLog.task_id == task_id)
    return query.order_by(models.AuditLog.timestamp.desc()).offset(skip).limit(limit).all()
