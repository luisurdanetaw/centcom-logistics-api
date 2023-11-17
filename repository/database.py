# repository.database.py
from fastapi import HTTPException
from mysql.connector import connect, Error



async def create_db_connection():
    try:
        connection = connect(
            user="root",
            password="centcom2023!",
            host="34.28.120.16",
            database="usf-sr-project-centcom",
        )
        print("creating connection")
        return connection
    except Error as e:
        print(f"Error: {e}")


async def find_all_where(table, field, hasValue):
    try:
        connection = await create_db_connection()
        with (connection.cursor(dictionary=True) as cursor):
            query = (
                f"SELECT * "
                f"FROM {table} "
                f"WHERE {table}.{field} = %s"
            )

            cursor.execute(query, (hasValue,))
            facilities = cursor.fetchall()
            if facilities is None:
                connection.close()
                raise HTTPException(status_code=404, detail="No results")

            connection.close()
            return facilities
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
