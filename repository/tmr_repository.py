from fastapi import FastAPI, Depends, HTTPException
from mysql.connector import MySQLConnection
from fastapi import HTTPException
from model.tmr import TMR
from repository.database import create_db_connection, find_all_where


async def find_all_tmrs_repository(facility_id: str = ""):
    try:
        return await find_all_where("tmrs", "facility_id", facility_id)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def create_tmr_repository(tmr_data: TMR):
    try:
        query = "INSERT INTO tmrs (requestor_id, cargo_description, quantity, units, id_num, requestor, date_received, facility_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        # Correctly await the create_db_connection coroutine
        connection = await create_db_connection()
        
        try:
            with (connection.cursor(dictionary=True) as cursor):
                cursor.execute(query, (tmr_data.requestor_id, tmr_data.cargo_description, tmr_data.quantity, tmr_data.units, tmr_data.id_num, tmr_data.requestor, tmr_data.date_received, tmr_data.facility_id,))
                connection.commit()
        finally:
            connection.close()

        return {"message": "TMR created successfully"}
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def update_tmr_repository(id: str, details: dict):

    try:
        connection = await create_db_connection()
        set_clause = ', '.join([f"{key} = %s" for key in details.keys()])
        values = list(details.values())

        # Execute the UPDATE statement
        update_query = f"UPDATE tmrs SET {set_clause} WHERE {id} = %s"

        with connection.cursor(dictionary=True) as cursor:
            cursor.execute(update_query, values + [id])
            connection.commit()

            # Fetch the updated row
            select_query = f"SELECT * FROM tmrs WHERE {id} = %s"
            cursor.execute(select_query, [id])
            updated_row = cursor.fetchone()
            connection.close()
            return updated_row

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=e)


