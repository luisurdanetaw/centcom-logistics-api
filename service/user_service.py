from model.user import User
import re
from repository.dummy_db import get_users, create_user, find_facility_repo
import bcrypt

from repository.user_repository import find_facility_repository


async def register_user(user: User):
    pattern = r'^(?=.*[a-zA-Z])(?=.*\d).+$'
    valid_password = bool(re.match(pattern, user.password))

    if valid_password:
        try:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            user_with_hashed_password = User(email=user.email, password=hashed_password.decode('utf-8'))
            created_user = await create_user(user_with_hashed_password)
            return created_user
        except Exception as e:
            print("Error creating user")
    else:
        raise ValueError("Password is not valid")


async def login_user(user: User):
    users = await get_users()
    found_user = next((u for u in users if u.email == user.email), None)

    return bool(found_user and bcrypt.checkpw(user.password.encode('utf-8'), found_user.password.encode('utf-8')))

async def find_facility_service(name:str = ""):
    return await find_facility_repository(name)
    #return await find_facility_repo(name)