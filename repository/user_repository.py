
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
