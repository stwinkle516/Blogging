import mysql.connector

# Connect to the MySQL database
connection = mysql.connector.connect(
    
    user="root",
    password="Mylifestyle",
    database="blogger"
)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Execute a SELECT query to retrieve data from the table
query = "SELECT * FROM users"
cursor.execute("SELECT * FROM users")

# Fetch all rows
rows = cursor.fetchall()

# Print the data
for row in rows:
    print(row)

# Close cursor and conne
