from starlette.exceptions import HTTPException

from repository.database import create_db_connection

async def find_all_tmrs_by_country(country):
    try:
        connection = await create_db_connection()
        with (connection.cursor(dictionary=True) as cursor):
            query = (
                f"SELECT * "
                f"FROM tmrs JOIN facilities ON tmrs.facility_id = facilities.id "
                f"WHERE country = %s"
            )

            cursor.execute(query, (country,))
            facilities = cursor.fetchall()
            if facilities is None:
                connection.close()
                raise HTTPException(status_code=404, detail="No results")

            connection.close()
            return facilities
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
