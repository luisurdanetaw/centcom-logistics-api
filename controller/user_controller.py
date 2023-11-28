# user_controller.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from model.user import User
from service.user_service import find_facility_service, get_supply_search_results_page, find_all_facilities_service
from repository.dummy_db import get_users
from fastapi.responses import JSONResponse
import mysql.connector
import re
import bcrypt

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

router = APIRouter()


# Define the User Pydantic model
class UserCreate(BaseModel):
    first_name: str = "NULL"
    last_name: str = "NULL"
    position: str = "NULL"
    email: str = "NULL"
    password: str = "NULL"
    phone: str = "NULL"


@router.get("/findFacility")
async def find_facility(name: str = ""):
    return await find_facility_service(name)

@router.get("/findAllFacilities")
async def find_all_facilities():
    return await find_all_facilities_service()

@router.get("/findFacilitiesWithSupplies")
async def find_facilities_with_supplies(user_id, supply, page: int = 1):
    #if page < 1:
       # return JSONResponse(content={"error": "Page must be >= 0"}, status_code=400)
    try:
        paginated_facilities, total_pages, total_results = await get_supply_search_results_page(user_id, supply, page)
        return JSONResponse(content={"results": paginated_facilities, "total_pages": total_pages, "total_results": total_results}, status_code=400)
    except HTTPException as http_exception:
        if http_exception.status_code == 404:
            return JSONResponse(content={"error": "No results found"}, status_code=404)
        else:
            return JSONResponse(content={"error": http_exception}, status_code=500)
    except Exception as e:
        return JSONResponse(content={"error": e}, status_code=500)



@router.post("/create")
async def create_user(user: UserCreate):
    try:
        if connection.is_connected():
            if not any(char.isupper() for char in user.password):
                raise HTTPException(status_code=400, detail="Password must contain at least one capitalized letter")
            if len(user.password) < 8:
                raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', user.password):
                raise HTTPException(status_code=400, detail="Password must contain at least one special character")
            if not re.match(r'^\d{3}-\d{3}-\d{4}$', user.phone):
                raise HTTPException(status_code=400, detail="Invalid phone number format. Please use XXX-XXX-XXXX format")
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            cursor = connection.cursor()
            # Insert the user into the database
            query = "INSERT INTO users (first_name, last_name, position, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (user.first_name, user.last_name, user.position, user.email, user.phone, user.password)
            print(values)
            cursor.execute(query, values)
            connection.commit()

            return {"message": "User created successfully"}
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": "Error creating user"}, status_code=500)
    
    



# Log in a user
@router.post("/login")
async def login(user: UserCreate):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            # Retrieve the user's password from the database
            query = "SELECT password FROM users WHERE email = %s"
            cursor.execute(query, (user.email,))
            result = cursor.fetchone()

            if result:
                print("result: ", result[0])
                print("user.password:", user.password)

                # Compare the plain text password with the stored password
                if user.password == result[0]:
                    return True
                else:
                    return False
            else:
                return "User not found"
    except mysql.connector.Error as e:
        print(e)
        return JSONResponse(content={"error": "Error logging in user"}, status_code=500)
