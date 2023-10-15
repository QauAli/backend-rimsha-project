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


def add_customer(self, C_Email_Id, Password, C_FirstName):
    query = f"INSERT INTO customer (C_Email_Id, Password, C_FirstName) VALUES ('{C_Email_Id}', '{Password}', '{C_FirstName}')"
    self.cursor.execute(query)
    self.connection.commit()

    def close(self):
        # Close the cursor and connection when done
        self.cursor.close()
        self.connection.close()

db = MyDatabase()
db.close()