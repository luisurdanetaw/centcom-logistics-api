# tmr_controller.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse

from service.tmr_service import find_all_tmrs_service

router = APIRouter()
@router.get("/findAll")
async def find_all_tmrs(facility_id: str = ""):
    try:
        return await find_all_tmrs_service(facility_id)
    except HTTPException as http_exception:
        if http_exception.status_code == 404:
            return JSONResponse(content={"error": "No results found"}, status_code=404)
        else:
            return JSONResponse(content={"error": http_exception}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": e}, status_code=500)