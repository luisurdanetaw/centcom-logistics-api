from repository.tmr_repository import find_all_tmrs_repository
from fastapi import HTTPException
import time

#Invalidate cache after 5 minutes
CACHE_TTL_SECONDS = 300
tmr_cache = {

}


async def find_all_tmrs_service(facility_id):
    try:
        tmrs, timestamp = tmr_cache.get(facility_id, (None, 0))
        current_time = time.time()

        if (current_time - timestamp <= CACHE_TTL_SECONDS) and (tmrs is not None):
            return tmrs
        elif tmrs is not None:
            del tmr_cache[facility_id]

        tmrs = await find_all_tmrs_repository(facility_id)
        tmr_cache[facility_id] = (tmrs, current_time)  # Store data and timestamp in cache
        return tmrs

    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
