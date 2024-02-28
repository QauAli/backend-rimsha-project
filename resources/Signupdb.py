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

    def signup_staff(self, Staff_Name, email, password):
        query = f"""
            INSERT INTO staff (Staff_Name, email, password) VALUES ('{Staff_Name}', '{email}', '{password}');
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return {"message": "Staff user created successfully"}
        except Exception as e:
            print(f"Error creating staff user: {e}")
            return None

    def signup_customer(self, C_FirstName, C_Email_Id, Password):
        query = f"""
            INSERT INTO customer (C_FirstName, C_Email_Id, Password) VALUES ('{C_FirstName}', '{C_Email_Id}', '{Password}');
        """
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return {"message": "Customer user created successfully"}
        except Exception as e:
            print(f"Error creating customer user: {e}")
            return None

    def close(self):
        # Close the cursor and connection when done
        self.cursor.close()
        self.connection.close()

db = MyDatabase()
db.close()
