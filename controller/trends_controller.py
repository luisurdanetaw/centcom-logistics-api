from fastapi import APIRouter
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
import mysql.connector

from repository.database import create_db_connection
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
async def tmrs_completed(country: str = ""):
    try:
        current_month_completed, change_percentage, delta = await tmrs_completed_service(country)
        return JSONResponse(
            content={
                "completed_current_month": current_month_completed,
                "change_percentage": change_percentage,
                "delta": delta
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
async def consumption(country: str = "", item_name: str = ""):
    cursor = connection.cursor()
    try:
        query = "SELECT consumption FROM inventory JOIN facilities ON inventory.facility_id = facilities.id WHERE country = %s AND item_name = %s"
        values = (country, item_name)
        cursor.execute(query, values)
        result = cursor.fetchone()
        return result
    except HTTPException as http_exception:
        print(http_exception.detail)

@router.get("/tmrsReceived")
async def tmrs_received(country: str = ""):
    try:
        current_month_received, change_percentage, delta = await tmrs_received_service(country)
        return JSONResponse(
            content={
                "received_current_month": current_month_received,
                "change_percentage": change_percentage,
                "delta": delta
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
async def shipment_speed(country: str = ""):
    try:
        current_month_speed, change_percentage, delta = await shipment_speed_service(country)
        return JSONResponse(
            content={
                "shipment_speed": current_month_speed,
                "change_percentage": change_percentage,
                "delta": delta
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
async def delayed_shipments(country: str = ""):
    try:
        current_month_delayed_shipments,change_percentage, delta = await delayed_shipments_service(country)
        return JSONResponse(
            content={
                "shipment_speed": current_month_delayed_shipments,
                "change_percentage": change_percentage,
                "delta": delta
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
async def top_requestors(country: str = ""):
    connect = await create_db_connection()
    cursor = connect.cursor()
    try:
        query = """
                SELECT requestor, COUNT(requestor) as request_count
                FROM tmrs JOIN facilities ON tmrs.facility_id = facilities.id
                WHERE country = %s
                GROUP BY requestor
                ORDER BY request_count DESC
                LIMIT 10;
                """
        cursor.execute(query, (country,))
        result = cursor.fetchall()
        connect.close()
        return result
    except HTTPException as http_exception:
        print(http_exception.detail)
