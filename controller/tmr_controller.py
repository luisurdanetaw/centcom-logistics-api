# tmr_controller.py
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from model.updateRequest import updateRequest
import mysql.connector
from model.tmr import TMR
from service.tmr_service import find_all_tmrs_service, create_tmr_service

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

# Helper function to check if an item exists in the inventory
def item_exists(cursor, facility_id, item_name):
    query = f"SELECT * FROM inventory WHERE facility_id = {facility_id} AND item_name = '{item_name}'"
    cursor.execute(query)
    return cursor.fetchone() is not None


@router.get("/findAll")
async def find_all_tmrs(facility_id: str = ""):
    try:
        return await find_all_tmrs_service(facility_id)
    except HTTPException as http_exception:
        if http_exception.status_code == 404:
            return JSONResponse(content={"error": "No results found"}, status_code=404)
        else:
            return JSONResponse(content={"error": str(http_exception.detail)}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.post("/createTMR")
async def create_tmr(tmr_create: TMR):
    try:
        # You might want to add validation logic here before calling the service
        result = await create_tmr_service(tmr_create)
        return JSONResponse(content={"message": "TMR created successfully", "data": result}, status_code=201)
    except HTTPException as http_exception:
        return JSONResponse(content={"error": str(http_exception.detail)}, status_code=http_exception.status_code)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@router.get("/inventory")
async def find_all_inventory(facility_id: str = ""):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            # Insert the user into the database
            query = "SELECT * FROM inventory"
            cursor.execute(query)
            connection.commit()
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": "Could not get inventory data"}, status_code=500)

@router.post("/update")
async def update_inventory(updateRequest: updateRequest):
    cursor = connection.cursor()
    try:
        # Check if the item exists
        if not item_exists(cursor, updateRequest.facility_id, updateRequest.item_name):
            # If not, insert a new record with the specified quantity
            insert_query = "INSERT INTO inventory (facility_id, item_name, quantity) VALUES (%s, %s, %s)"
            values = (updateRequest.facility_id, updateRequest.item_name, updateRequest.quantity)
            cursor.execute(insert_query, values)
            connection.commit()
        else:
            # If it exists, update the quantity
            update_query = "UPDATE inventory SET quantity = quantity + %s WHERE facility_id = %s AND item_name = %s"
            values = (updateRequest.quantity, updateRequest.facility_id, updateRequest.item_name, )
            cursor.execute(update_query, values)
            connection.commit()
        
        update_query = "UPDATE facilities f \
                        SET status = ( \
                            SELECT \
                                CASE \
                                    WHEN COUNT(*) = SUM(CASE WHEN i.status = 'green' THEN 1 ELSE 0 END) THEN 'green' \
                                    WHEN SUM(CASE WHEN i.status = 'yellow' THEN 1 ELSE 0 END) > 0 THEN 'yellow' \
                                    ELSE 'black' \
                                END \
                            FROM inventory i \
                            WHERE f.id = i.facility_id \
                        )"
        cursor.execute(update_query)
        connection.commit()

        update_query = "UPDATE inventory \
                        SET \
                            status = \
                                CASE \
                                    WHEN quantity >= 0.75 * stockage_objective THEN 'Green' \
                                    WHEN quantity >= 0.5 * stockage_objective AND quantity < 0.75 * stockage_objective THEN 'Yellow' \
                                    ELSE 'Black' \
                        END"
        cursor.execute(update_query)
        connection.commit()

        return {"message": "Inventory updated successfully"}

    except Exception as e:
        print(e)
        return JSONResponse(content={"error": "Could not update inventory data"}, status_code=500)


# @router.post("/add")
# async def add_inventory(facility_id: str = ""):
#     try:
        
        
#     except Exception as e:
#         print(e)
#         return JSONResponse(content={"error": "Could not add inventory data"}, status_code=500)

# @router.post("/remove")
# async def remove_inventory(facility_id: str = "":)
#     try:
        
        
#     except Exception as e:
#         print(e)
#         return JSONResponse(content={"error": "Could not remove inventory data"}, status_code=500)
