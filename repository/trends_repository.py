from starlette.exceptions import HTTPException

from repository.database import find_all_where


async def tmrs_completed_repository(facility_id: str = ""):
    try:
        tmrs = await find_all_where('tmrs', 'facility_id', facility_id)

        if len(tmrs) == 0:
            raise HTTPException(status_code=404, detail="Facility not found")
        else:
            return tmrs

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail='Internal Server Error')