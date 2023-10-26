
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


