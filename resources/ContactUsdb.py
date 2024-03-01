import mysql.connector

class MyDatabase:
    def __init__(self):
# Establish a connection to the MySQL server
     self.connection = mysql.connector.connect(
    host="localhost",  # Replace with your MySQL server host
    user="root",        # Replace with your MySQL username
    password="",        # Replace with your MySQL password
    database="motor menders"  # Replace with the name of your database
)
# Create a cursor object to interact with the database
     self.cursor = self.connection.cursor()

    def add_Contactform(self, FirstName, LastName, Email_id, Message):
     query = f"INSERT INTO contact_us (FirstName, LastName, Email_id, Message) VALUES ('{FirstName}', '{LastName}', '{Email_id}', '{Message}')"
     print("Query:", query)  # Add this line to print the query

     try:
        self.cursor.execute(query)
        self.connection.commit()
     except Exception as e:
        print(f"Error inserting data into the database: {e}")
        return None



    def close(self):
# Close the cursor and connection when done
      self.cursor.close()
      self.connection.close()


# Create an instance of the MyDatabase class
db = MyDatabase()
db.close()
