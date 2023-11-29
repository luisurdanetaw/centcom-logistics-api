# tmr_service.py
from repository.tmr_repository import find_all_tmrs_repository, create_tmr_repository, update_tmr_repository
from fastapi import HTTPException
from model.tmr import TMR
import time

from repository.trends_repository import consumption_repository

CACHE_TTL_SECONDS = 300
tmr_cache = {}


async def find_all_tmrs_service(facility_id):
    try:
        tmrs, timestamp = tmr_cache.get(facility_id, (None, 0))
        current_time = time.time()

        if (current_time - timestamp <= CACHE_TTL_SECONDS) and (tmrs is not None):
            return tmrs
        elif tmrs is not None:
            del tmr_cache[facility_id]

        tmrs = await find_all_tmrs_repository(facility_id)
        tmr_cache[facility_id] = (tmrs, current_time)
        return tmrs

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_tmr_service(tmr_data: TMR):
    try:
        # You can add additional validation logic here before interacting with the repository
        # For example, you might want to ensure that required fields are present before proceeding
        if not tmr_data.requestor_id or not tmr_data.cargo_description:
            raise HTTPException(status_code=400, detail="requestor_id and cargo_description are required fields")
        # Input validation: Check if the requestor contains only alphabetical characters
        if not tmr_data.requestor or not all(char.isalpha() or char.isspace() for char in tmr_data.requestor):
            raise HTTPException(status_code=400, detail="Requestor must contain only alphabetical characters and spaces")


        created_tmr = await create_tmr_repository(tmr_data)
        return created_tmr
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_tmr_service(id: str, details: dict):
    try:
        return await update_tmr_repository(id, details)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def consumption_service(country: str):
    try:
        if len(country) != 3:
            raise HTTPException(status_code=400, detail='COUNTRY CODE NEEDS TO BE 3 FREAKING LETTERS')
        else:
            return await consumption_repository(country)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))