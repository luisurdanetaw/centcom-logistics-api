import bcrypt
from model.user import User


inventoryTwo = {
    'Ammo': {
        'quantity': 10000,
        'so': 15000,
        'cf': 5500,
        'class': 'III'
    },
    'MRE': {
        'quantity': 230000,
        'so': 300000,
        'cf': 11500,
        'class': 'I'
    }
}


facility = {
    'name': 'Fort Moore',
    'location': 'GA',
    'co': 'Maj. Luis Urdaneta',
    'email': 'luisurdaneta@army.mil',
    'status': 'red',
    'phone': '3054128032',
    'inventory': {
        'Gas': {
            'quantity': 10000,
            'so': 15000,
            'cf': 6240,
            'class': 'IV'

        },
        'Water': {
            'quantity': 20000,
            'so': 30000,
            'cf': 8400,
            'class': 'I'
        }
    }
}
facilityTwo = {
    'name': 'Test Base',
    'location': 'FL',
    'co': 'Col. John Smith',
    'email': 'johnsmith@army.mil',
    'status': 'green',
    'phone': '8133043232',
    'inventory': inventoryTwo
}

password = "1234"
hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
test_user = User(email="tester@gmail.com", password=hashed_password.decode('utf-8'))
users = []
facilities = []
facilities.append(facility)
facilities.append(facilityTwo)
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

async def find_facility_repo(name:str=""):
    try:
        for facility in facilities:
            if facility['name'].lower() == name:
                return facility

        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

