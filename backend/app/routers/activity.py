from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from ..schemas import ActivityOut
from ..deps import get_current_user
from ..database import get_db_session
from ..models import ActivityLog

router = APIRouter()

@router.get("", response_model=List[ActivityOut])
async def get_activity_logs(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    # Get recent activity logs
    logs = db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).limit(50).all()
    
    return logs


