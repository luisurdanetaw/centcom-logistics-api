import bcrypt
from model.user import User


password = "1234"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
test_user = User(email="tester@gmail.com", password=hashed_password.decode('utf-8'))
users = []
users.append(test_user)
print("TEST USER PASSWORD: ", test_user.password)

async def get_users():
    print(type(users))
    return users

async def create_user(user:User):
    print("called")
    try:
        users.append(user)
        return user.email
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
