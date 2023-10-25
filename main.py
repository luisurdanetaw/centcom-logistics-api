from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from controller import user_controller
import mysql.connector


# Define the database connection parameters
host = "localhost"  # Replace with your database host
user = "new_user"  # Replace with your database username
password = "password"  # Replace with your database password
database = "CENTCOM"  # Replace with your database name

app = FastAPI()

origins = [
    "http://localhost:3000",  # Replace with the origin of your frontend (e.g., http://yourfrontend.com)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def read_root():
    return {"message": "CENTCOM Logistics API"}

@app.get("/test")
def read_root():
    connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
    )

    if connection.is_connected():
        print("Connected to the database")
        cursor = connection.cursor()
    else:
        print("Failed to connect to the database")
        query = "SELECT * FROM user"
        cursor.execute(query)
    for row in cursor.fetchall():
        print(row)

    if connection.is_connected():
        cursor.close()
        connection.close()
    return {"message": "CENTCOM Logistics API"}

app.include_router(user_controller.router, prefix="/user")
