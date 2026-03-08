from fastapi import APIRouter, Depends, HTTPException
from dependencies import use_session, verification
from Schemas import ServiceSchema
from Models import Refuel, User
from sqlalchemy.orm import Session

user_router = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(verification)])

@user_router.post("/Service")
async def service(service_schema: ServiceSchema, session: Session=Depends(use_session), user: User=Depends(verification)):
    new_service = Refuel(user=id, fuel_type=service_schema.fuel_type, liters=service_schema.liters, status="REQUESTED")
    new_service.price()
    user.cashback += new_service.bonus
    session.add(new_service)
    session.commit()
    session.refresh(new_service)
    return {
        "status": new_service.status,
        "message":"Please proceed to the next step."
    }

@user_router.post("/service/cancel/{id_request}")
async def cancel(id_request: int, session: Session=Depends(use_session), user: User=Depends(verification)):
    service = session.query(Refuel).filter(Refuel.id_request==id_request).first()
    if not service:
        raise HTTPException(status_code=400, detail="Order not found.")
    if not user.admin and service.id_user != user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to make this modification.")
    if Refuel.status != "REQUESTED":
        raise HTTPException(status_code=400, detail="Cannot cancel this service.")
    
    if user.admin == Refuel.user:
        message = f"The recharge service for number {service.id_service} has been cancelled by an administrator: To find out why, please visit our support."
    else:
        message = f"The service to replenish number {service.id_service} has been cancelled.", 


    service.status = "CANCELLED"
    session.commit()
    return {
        "message": message,
        "service": service
    }

"""
REQUESTED
APPROVED
CANCELLED
FINISHED

"""