from database import get_db_connection

print("Testing MySQL connection...")

connection = get_db_connection()

if connection:
    print("SUCCESS: Connected to MySQL!")
    print("Database:", connection.database)
    connection.close()
    print("Connection closed.")
else:
    print("FAILED: Could not connect to MySQL.")