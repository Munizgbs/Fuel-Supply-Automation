from fastapi import APIRouter, Depends
from dependencies import UseSession
from schemas import ServiceSchema
from models import Service
from sqlalchemy.orm import Session

user_router = APIRouter(prefix="/user", tags=["user"])

@user_router.post("/refuel")
async def start_refueling(service_schema: ServiceSchema, session: Session=Depends(UseSession)):
    service = Service(service_schema.typee, service_schema.liters)
    if service_schema.typee == "GASOLINE":
        value = service_schema.liters * 6.31
    if service_schema.typee == "DIESEL":
        value = service_schema.liters * 6,12
    if service_schema.typee == "ETHANOL":
        value = service_schema.liters * 4,64
    Service.value = value
    session.add(service)
    session.commit()
    return {"message":"The service has started, please complete the next step."}