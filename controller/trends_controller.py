from fastapi import APIRouter
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
import mysql.connector

from service.trends_service import tmrs_completed_service, tmrs_received_service

# Define the database connection parameters
host = "34.28.120.16"  # Replace with your database host
user = "root"  # Replace with your database username
password = "centcom2023!"  # Replace with your database password
database = "usf-sr-project-centcom"  # Replace with your database name

connection = mysql.connector.connect(
host=host,
user=user,
password=password,
database=database
)

router = APIRouter()

@router.get("/tmrsCompleted")
async def tmrs_completed(facility_id: str = ""):
    cursor = connection.cursor()
    try:
        current_month_completed, delta = await tmrs_completed_service(facility_id)
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

@router.get("/consumption")
async def consumption(facility_id: str = "", item_name: str = ""):
    cursor = connection.cursor()
    try:
        query = "SELECT consumption FROM inventory WHERE facility_id = %s AND item_name = %s"
        values = (facility_id, item_name)
        cursor.execute(query, values)
        result = cursor.fetchone()
        print (result)
        return result
    except HTTPException as http_exception:
        print(http_exception.detail)
        print(result)

@router.get("/tmrsReceived")
async def tmrs_received(facility_id: str = ""):
    try:
        current_month_received, delta = await tmrs_received_service(facility_id)
        return JSONResponse(
            content={
                "received_current_month": current_month_received,
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