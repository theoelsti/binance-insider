import mysql.connector

# Connect to the database
conn = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="yourdatabase"
)


# Handle error 
# Insert function
def insert(query):
  cursor = conn.cursor()
  cursor.execute(query)
  conn.commit()
  

# Select function
def select_users():
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

# Close the connection
conn.close()
