from model.user import User

test_user = User(email="tester@gmail.com", password="1234")
users = []
users.append(test_user)

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
