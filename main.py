from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from controller import user_controller
import mysql.connector


# Define the database connection parameters
host = "34.28.120.16"  # Replace with your database host
user = "root"  # Replace with your database username
password = "centcom2023!"  # Replace with your database password
database = "usf-sr-project-centcom"  # Replace with your database name

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

app = FastAPI()

origins = [
    "http://localhost:3000",  # Replace with the origin of your frontend (e.g., http://yourfrontend.com)
    "http://127.0.0.1:3000"
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
    query = "SELECT * FROM users"
    cursor.execute(query)
    for row in cursor.fetchall():
        print(row)
    return {"message": "CENTCOM Logistics API"}

app.include_router(user_controller.router, prefix="/user")
# app.include_router(tmr_controller.router, prefix="/tmr")
