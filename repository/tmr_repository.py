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
    

async def find_all_tmrs_by_country(country: str = ""):
    try:
        return await find_all_where("tmrs JOIN facilities ON tmrs.facility_id = facilities.id","country", country)
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



        