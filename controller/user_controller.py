# user_controller.py
from fastapi import APIRouter
from pydantic import BaseModel
from model.user import User
from service.user_service import register_user, login_user, find_facility_service
from repository.dummy_db import get_users
from fastapi.responses import JSONResponse


router = APIRouter()

#/user
@router.get("/findAll")
async def get_all_users():
   users = await get_users()
   return users

@router.get("/findFacility")
async def find_facility(name: str = ""):
   return await find_facility_service(name)


@router.post("/create")
async def create_user(user: User):
    created_user = await register_user(user)
    return created_user

@router.post("/login")
async def login(user: User):
    loggedIn = await login_user(user)
    return loggedIn