from fastapi import HTTPException

from model.user import User
import re
from repository.dummy_db import get_users, create_user, find_facility_repo
import bcrypt
from model.user import User
from repository.user_repository import find_facility_repository, find_facilities_with_supplies_repository, \
    find_all_facilities_repository
import re

from fastapi import FastAPI
search_cache = {

}
async def find_facility_service(name:str = ""):
    return await find_facility_repository(name)


async def find_facilities_with_supplies(user_id, supply):
    try:
        facilities = await find_facilities_with_supplies_repository(supply)
        await insert_results_into_cache(user_id, supply, facilities)

    except HTTPException as http_exception:
        if http_exception.status_code == 404:
            print(http_exception)
            raise HTTPException(status_code=404, detail=str(http_exception.detail))
        else:
            print(http_exception)
            raise HTTPException(status_code=500, detail=str(http_exception.detail))
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


async def get_supply_search_results_page(user_id, supply, page):
    page_size = 5
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    if user_id not in search_cache or search_cache[user_id]['supply'] != supply:
        try:
            await find_facilities_with_supplies(user_id, supply)
        except HTTPException as e:
            print(e)
            raise HTTPException(status_code=e.status_code, detail=str(e))

    try:
        facilities = search_cache[user_id]['results']
        paginated_facilities = facilities[start_idx:end_idx]

        total_pages = len(facilities)//page_size
        if len(facilities) % page_size != 0:
            total_pages += 1

        return paginated_facilities, total_pages, len(facilities)
    except KeyError as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


async def insert_results_into_cache(user_id, supply, results):
    search_cache[user_id] = {
        'results': results,
        'supply': supply,
    }



async def create_user_service(email: str, password: str):
    # Validate password using regex
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character")

    # Hash the password using bcrypt before storing it in the database
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Call the repository function to create the user
    user = await create_user(email, hashed_password)

    return user


async def find_all_facilities_service():
    try:
        facilities = await find_all_facilities_repository()
        return list(map(lambda x: x["name"], filter(lambda x: x is not None, facilities)))

    except HTTPException as http_exception:
        raise http_exception

