
from fastapi import FastAPI, Depends, HTTPException
from mysql.connector import MySQLConnection
from fastapi import HTTPException
from repository.database import create_db_connection

async def find_facility_repository(name: str = ""):
    try:
        connection = await create_db_connection()
        with connection.cursor() as cursor:
            # Pass the parameter as a tuple with a single element
            cursor.execute("SELECT * FROM facilities WHERE name = %s", (name,))
            facility = cursor.fetchone()
            if facility is None:
                raise HTTPException(status_code=404, detail="Facility not found")

            keys = [
                "id",
                "name",
                "country",
                "state",
                "zipcode",
                "co",
                "co_email",
                "co_phone",
                "status"
            ]
            data = {key: value for key, value in zip(keys, facility)}
            connection.close()
            return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def getFacilityInventory(facility_id: int):
    connection = await create_db_connection()
    with connection.cursor(dictionary=True) as cursor:
        # Pass the parameter as a tuple with a single element
        cursor.execute("SELECT * FROM inventory WHERE facility_id = %d", (facility_id,))
        inventory = cursor.fetchone()
        if inventory is None:
            raise HTTPException(status_code=404, detail="Facility not found")

        connection.close()
        return inventory
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
