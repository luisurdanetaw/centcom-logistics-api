from model.user import User
from model.tmr import Tmr

test_user = User(email="tester@gmail.com", password="1234")
users = []
tmrs = []
users.append(test_user)

async def get_users():
    print(type(users))
    return users

async def create_user(user:User):
    print("called create user")
    try:
        users.append(user)
        return user.email
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

async def create_tmr(tmr: Tmr):
    print("called create tmr")
    try:
        print(tmrs)
        tmrs.append(tmr)
        print(tmrs)
        return tmr.id_num
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
