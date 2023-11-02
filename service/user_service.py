from fastapi import HTTPException

from model.user import User
import re
from repository.dummy_db import get_users, create_user, find_facility_repo
import bcrypt
from model.user import User
from repository.user_repository import find_facility_repository, find_facilities_with_supplies_repository

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
            raise HTTPException(status_code=404, detail=str(http_exception.detail))
        else:
            raise HTTPException(status_code=500, detail=str(http_exception.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_supply_search_results_page(user_id, supply, page=0):

    page_size = 10
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size

    if (search_cache[user_id].supply != supply) or (search_cache[user_id] is None):
        try:
            await find_facilities_with_supplies(user_id, supply)
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=str(e))

    facilities = search_cache["search_results"]
    paginated_facilities = facilities[start_idx:end_idx]
    return paginated_facilities



async def insert_results_into_cache(userId, supply, results):
    search_cache[userId] = {
        'results': results,
        'supply': supply
    }



# from model.user import User
# import re
# from repository.dummy_db import get_users, create_user
# import bcrypt

# async def register_user(user: User):
#     pattern = r'^(?=.*[a-zA-Z])(?=.*\d).+$'
#     valid_password = bool(re.match(pattern, user.password))

#     if valid_password:
#         try:
#             hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
#             user_with_hashed_password = User(email=user.email, password=hashed_password.decode('utf-8'))
#             created_user = await create_user(user_with_hashed_password)
#             return created_user
#         except Exception as e:
#             print("Error creating user")
#     else:
#         raise ValueError("Password is not valid")


# async def login_user(user: User):
#     users = await get_users()
#     found_user = next((u for u in users if u.email == user.email), None)

#     return bool(found_user and bcrypt.checkpw(user.password.encode('utf-8'), found_user.password.encode('utf-8')))
