# import mysql.connector

# # Establish a connection to the MySQL database
# mydb = mysql.connector.connect(
#     host="127.0.0.1",
#     user="root",
#     password="Hulkiscool",
#     database="CENTCOM"
# )

# # Check if the connection is successful
# if mydb.is_connected():
#     print("Connected to the MySQL database!")

#     # Create a cursor object to interact with the database
#     cursor = mydb.cursor()

#     # Define the SQL query to retrieve data from the 'users' table
#     query = "SELECT * FROM users"

#     # Execute the query
#     cursor.execute(query)

#     # Fetch all the rows from the 'users' table
#     users = cursor.fetchall()

#     # Print the retrieved data
#     print("Users in the 'users' table:")
#     for user in users:
#         print(user)

#     # Close the cursor and database connection
#     cursor.close()
#     mydb.close()

# else:
#     print("Failed to connect to the MySQL database.")

import mysql.connector
from datetime import datetime

# Establish a connection to the MySQL database
mydb = mysql.connector.connect(
    host="34.28.120.16",
    user="root",
    password="centcom2023!",
    database="usf-sr-project-centcom"
)

# Check if the connection is successful
if mydb.is_connected():
    print("Connected to the MySQL database!")

    # Create a cursor object to interact with the database
    cursor = mydb.cursor()

    # Define the SQL query to retrieve TMRs from the 'tmrs' table for the requestor 'mahin'
    query = "SELECT * FROM tmrs WHERE requestor = 'mahin'"

    # Execute the query
    cursor.execute(query)

    # Fetch all the rows from the 'tmrs' table for the requestor 'mahin'
    tmrs = cursor.fetchall()

    # Print the retrieved TMRs with formatted dates
    print("TMRs for requestor 'mahin':")
    for tmr in tmrs:
        formatted_tmr = list(tmr)
        # Convert date objects to formatted strings
        formatted_tmr[5] = tmr[5].strftime('%Y-%m-%d')  #
        formatted_tmr[6] = tmr[6].strftime('%Y-%m-%d')  # 
        formatted_tmr[17] = tmr[17].strftime('%Y-%m-%d')  # 
        formatted_tmr[18] = tmr[18].strftime('%Y-%m-%d')  # 
        formatted_tmr[19] = tmr[19].strftime('%Y-%m-%d')  # 
        formatted_tmr[20] = tmr[20].strftime('%Y-%m-%d')  # 
        print(tuple(formatted_tmr))

    # Close the cursor and database connection
    cursor.close()
    mydb.close()

else:
    print("Failed to connect to the MySQL database.")


