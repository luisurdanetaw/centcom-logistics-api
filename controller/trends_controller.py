from fastapi import APIRouter
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse

from service.trends_service import tmrs_completed_service

router = APIRouter()

@router.get("/tmrsCompleted")
async def tmrs_completed(facility_id: str = ""):
    try:
        current_month_completed, delta =  await tmrs_completed_service(facility_id)
        return JSONResponse(
            content={
                "completed_current_month": current_month_completed,
                "change": delta
            }, status_code=200)
    except HTTPException as http_exception:
        print(http_exception.detail)
        if http_exception.status_code == 404:
            return JSONResponse(content={"error": "No results found"}, status_code=404)
        else:
            return JSONResponse(content={"error": str("Internal Server error")}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str("Internal Server Error")}, status_code=500)