from model.user import User
import re
from repository.dummy_db import get_users, create_user, find_facility_repo
import bcrypt
from model.user import User
from repository.user_repository import find_facility_repository

# Create a function to register a user
def register_user(user: User):
    pattern = r'^(?=.*[a-zA-Z])(?=.*\d).+$'
    valid_password = bool(re.match(pattern, user.password))

    if valid_password:
        try:
            if connection.is_connected():
                cursor = connection.cursor()

                # Hash the password
                hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
                user_with_hashed_password = User(email=user.email, password=hashed_password.decode('utf-8'))

                # Insert the user into the database
                insert_query = "INSERT INTO users (email, password) VALUES (%s, %s)"
                cursor.execute(insert_query, (user_with_hashed_password.email, user_with_hashed_password.password))
                connection.commit()

                return user_with_hashed_password
        except Exception as e:
            print("Error creating user:", e)
    else:
        raise ValueError("Password is not valid")

# Create a function to log in a user
def login_user(user: User):
    try:
        if connection.is_connected():
            cursor = connection.cursor()

            # Retrieve the user from the database
            select_query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(select_query, (user.email,))
            found_user = cursor.fetchone()

            if found_user:
                # Check the hashed password
                if bcrypt.checkpw(user.password.encode('utf-8'), found_user[1].encode('utf-8')):
                    return True
        return False
    except Exception as e:
        print("Error logging in:", e)
        return False

async def find_facility_service(name:str = ""):
    return await find_facility_repository(name)
    #return await find_facility_repo(name)

# from model.user import User
# import re
# from repository.dummy_db import get_users, create_user
# import bcrypt

# async def register_user(user: User):
#     pattern = r'^(?=.*[a-zA-Z])(?=.*\d).+$'
#     valid_password = bool(re.match(pattern, user.password))

#     if valid_password:
#         try:
#             hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
#             user_with_hashed_password = User(email=user.email, password=hashed_password.decode('utf-8'))
#             created_user = await create_user(user_with_hashed_password)
#             return created_user
#         except Exception as e:
#             print("Error creating user")
#     else:
#         raise ValueError("Password is not valid")


# async def login_user(user: User):
#     users = await get_users()
#     found_user = next((u for u in users if u.email == user.email), None)

#     return bool(found_user and bcrypt.checkpw(user.password.encode('utf-8'), found_user.password.encode('utf-8')))
