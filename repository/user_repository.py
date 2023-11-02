
from fastapi import FastAPI, Depends, HTTPException
from mysql.connector import MySQLConnection
from fastapi import HTTPException
from repository.database import create_db_connection

async def find_facility_repository(name: str = ""):
    try:
        connection = await create_db_connection()
        with connection.cursor(dictionary=True) as cursor:
            # Pass the parameter as a tuple with a single element
            cursor.execute("SELECT * FROM facilities WHERE name = %s", (name,))
            facility = cursor.fetchone()
            if facility is None:
                raise HTTPException(status_code=404, detail="Facility not found")


            cursor.execute("SELECT * FROM inventory WHERE facility_id = %s", (facility['id'],))
            inventory = cursor.fetchall()

            facility['inventory'] = inventory
            connection.close()
            return facility
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def find_facilities_with_supplies_repository(supply: str = ""):
    try:
        connection = await create_db_connection()
        with (connection.cursor(dictionary=True) as cursor):
            query = (
                "SELECT facilities.*, inventory.quantity, inventory.stockage_objective, inventory.consumption "
                "FROM facilities "
                "INNER JOIN inventory " 
                "ON facilities.id = inventory.facility_id "
                "WHERE inventory.item_name = %s"
            )

            cursor.execute(query, (supply,))
            facilities = cursor.fetchall()
            if facilities is None:
                raise HTTPException(status_code=404, detail="No results")

            return facilities
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

