from fastapi import APIRouter, Depends, HTTPException
from models import User, Service
from dependencies import use_session, verification, administrator
from sqlalchemy.orm import Session

admin_router = APIRouter(prefix="/administrator", tags=["administrator"], dependecies=[Depends(administrator)])

@admin_router.get("/list")
async def history(session: Session=Depends(use_session), user: User=Depends(verification)):
        services = session.query(Service).all()
        return {
            "history": services
        }
    