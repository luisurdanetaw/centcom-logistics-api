from fastapi import APIRouter
from pydantic import BaseModel
from model.user import User
from service.user_service import register_user, login_user
from fastapi.responses import JSONResponse
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

router = APIRouter()

# Define the User Pydantic model
class UserCreate(BaseModel):
    id: int = 0
    first_name: str = "NULL"
    last_name: str = "NULL"
    position: str = "NULL"
    email: str = "NULL"
    password: str ="NULL"
    phone: str = "NULL"

# Create a user
@router.post("/create")
async def create_user(user: UserCreate):
    try:
        if connection.is_connected():
            cursor = connection.cursor()
            # Insert the user into the database
            query = "INSERT INTO user (first_name, last_name, position, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (user.first_name, user.last_name, user.position, user.email, user.phone, user.password)
            print(values)
            cursor.execute(query, values)
            connection.commit()

            return {"message": "User created successfully"}
    except Exception as e:
        return JSONResponse(content={"error": "Error creating user"}, status_code=500)
    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()

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
                    return "Login successful"
                else:
                    return "Invalid email or password"
            else:
                return "User not found"
    except mysql.connector.Error as e:
        print(e)
        return JSONResponse(content={"error": "Error logging in user"}, status_code=500)
    # finally:
    #     if connection.is_connected():
    #         cursor.close()
    #         connection.close()




# async def login(user: UserCreate):
#     cursor = connection.cursor()
#     try:
#         # Retrieve the user from the database
#         query = "SELECT * FROM users WHERE email = %s"
#         cursor.execute(query, (user.email,))
#         found_user = cursor.fetchone()

#         if found_user:
#             # Check the hashed password (using bcrypt or your chosen method)
#             if found_user[1] == "hashed_password_here":  # Replace with actual hashed password
#                 return {"message": "Login successful"}
        
#         return JSONResponse(content={"error": "Invalid email or password"}, status_code=400)
#     except Exception as e:
#         return JSONResponse(content={"error": "Error logging in"}, status_code=500)
#     finally:
#         if connection.is_connected():
#             cursor.close()
            # connection.close()



# # user_controller.py
# from fastapi import APIRouter
# from pydantic import BaseModel
# from model.user import User
# from service.user_service import register_user, login_user
# from repository.dummy_db import get_users
# from fastapi.responses import JSONResponse

# router = APIRouter()

# #/user
# @router.get("/findAll")
# async def get_all_users():
#    users = await get_users()
#    return users

# @router.post("/create")
# async def create_user(user: User):
#     created_user = await register_user(user)
#     return created_user

# @router.post("/login")
# async def login(user: User):
#     loggedIn = await login_user(user)
#     return loggedIn