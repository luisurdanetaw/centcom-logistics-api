from fastapi import APIRouter
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
import mysql.connector

from service.trends_service import tmrs_completed_service, tmrs_received_service, shipment_speed_service, \
    delayed_shipments_service

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
        return result
    except HTTPException as http_exception:
        print(http_exception.detail)

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



@router.get("/shipmentSpeed")
async def shipment_speed(facility_id: str = ""):
    try:
        current_month_speed, delta = await shipment_speed_service(facility_id)
        return JSONResponse(
            content={
                "shipment_speed": current_month_speed,
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


@router.get("/delayedShipments")
async def delayed_shipments(facility_id: str = ""):
    try:
        current_month_delayed_shipments, delta = await delayed_shipments_service(facility_id)
        return JSONResponse(
            content={
                "shipment_speed": current_month_delayed_shipments,
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

    
@router.get("/topRequestors")
async def top_requestors(facility_id: str = ""):
    cursor = connection.cursor()
    try:
        query = """
                SELECT requestor, COUNT(requestor) as request_count
                FROM tmrs
                WHERE facility_id = %s
                GROUP BY requestor
                ORDER BY request_count DESC
                LIMIT 10;
                """
        cursor.execute(query, (facility_id,))
        result = cursor.fetchall()
        return result
    except HTTPException as http_exception:
        print(http_exception.detail)
