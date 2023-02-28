import mysql.connector

# Get user input for database name and table name
#db_name = input("Enter database name: ")
table_name = input("Enter table name: ")

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="pass",
    database='horizon_travels_test'
)
cursor = mydb.cursor()

# Get column names for table
cursor.execute(f"DESCRIBE {table_name}")
columns = [row[0] for row in cursor.fetchall()]

# Get user input for values to be inserted into table
values = []
for column in columns:
    value = input(f"Enter value for {column}: ")
    values.append(value)

# Construct SQL query to insert data into table
query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s' for _ in columns])})"
cursor.execute(query, values)
mydb.commit()

# Close database connection
cursor.close()
mydb.close()

print("Data inserted successfully!")
