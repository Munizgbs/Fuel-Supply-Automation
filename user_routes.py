from fastapi import APIRouter, Depends, HTTPException
from dependencies import use_session, verification
from schemas import ServiceSchema
from models import Service, User
from sqlalchemy.orm import Session

user_router = APIRouter(prefix="/user", tags=["user"], dependencies=[Depends(verification)])

@user_router.post("/request_service")
async def refuel(service_schema: ServiceSchema, session: Session=Depends(use_session), user: User=Depends(verification)):
    new_service = Service(user=id, fuel_type=service_schema.fuel_type, liters=service_schema.liters, status="REQUESTED")
    session.add(new_service)
    session.commit()
    session.refresh(new_service)
    return {"message":"The service has started, please complete the next step."}

@user_router.post("/refuel/cancel/{id_service}")
async def cancel(id_service: int, session: Session=Depends(use_session), user: User=Depends(verification)):
    service = session.query(Service).filter(Service.id_service==id_service).first()
    if not service:
        raise HTTPException(status_code=400, detail="Order not found.")
    if not user.admin and user != service.user:
        raise HTTPException(status_code=403, detail="You are not authorized to make this modification.")
    if service.status != "REQUESTED":
        raise HTTPException(status_code=400, detail="Cannot cancel this service.")
    service.status = "CANCELED"
    session.commit()
    return {
        "message": f"supply service number {service.id_service} canceled by user: {service.id_user}",
        "service": service
    }

#Cliente cria serviço → status = REQUESTED
#Admin aprova → status = APPROVED
#Sistema calcula preço
#Finaliza → status = COMPLETED
#Cliente pode cancelar apenas se estiver REQUESTED