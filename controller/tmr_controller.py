# tmr_ticket_controller.py
from fastapi import APIRouter
from pydantic import BaseModel
from model.tmr import Tmr
import service.tmr_service as tmr_service
# from repository.dummy_db import get_users
from fastapi.responses import JSONResponse

router = APIRouter()

#/tmr

@router.post("/create/")
async def create_tmr(tmr: Tmr):
    try:
        return await tmr_service.create_tmr(tmr)
    except Exception as e:
        return -1

# @router.get("/findAll/")
# async def get_all_users():
#    users = await get_users()
#    return users


