from fastapi import APIRouter, Depends, HTTPException
from Models import User, Refuel
from dependencies import use_session, verification, administrator
from sqlalchemy.orm import Session

admin_router = APIRouter(prefix="/administrator", tags=["administrator"], dependencies=[Depends(administrator)])

@admin_router.get("/list")
async def history(session: Session=Depends(use_session), user: User=Depends(verification)):
        services = session.query(Refuel).all()
        return {
            "history": services
        }

@admin_router.get("/list/request_view/{id_request}")
async def view_list(id_request, session: Session=Depends(use_session), user: User=Depends(verification)):
      services = session.query(Refuel).filter(Refuel.id_request==id_request).all()
      return services

@admin_router.get("/request_view/{id_request}")
async def view(id_request, session: Session=Depends(use_session), user: User=Depends(verification)):
        service = session.query(Refuel).filter(Refuel.id==id_request).first()
        if not service:
            raise HTTPException(status_code=400, detail="Order not found.")
        return {
              "information": service
        }