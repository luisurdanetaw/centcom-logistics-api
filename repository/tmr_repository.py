from fastapi import FastAPI, Depends, HTTPException
from mysql.connector import MySQLConnection
from fastapi import HTTPException
from repository.database import create_db_connection, find_all_where


async def find_all_tmrs_repository(facility_id: str = ""):
    try:
        return await find_all_where("tmrs", "facility_id", facility_id)
    except HTTPException as http_exception:
        raise http_exception
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))