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

    def add_admin(self,Admin_id, body):
        query = f"INSERT INTO admin (Admin_id, name, email, password) VALUES ( '{Admin_id}','{body['name']}', '{body['email']}', '{body['password']}')"
        self.cursor.execute(query)
        self.connection.commit()

    def update_admin(self, Admin_id, body):
        query = f"UPDATE admin SET password='{body['password']}', name='{body['name']}' WHERE Admin_id='{Admin_id}'"
        print(query)
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return 0
        else:
            self.connection.commit()
            return 1


    def delete_admin(self, Admin_id):
        query = f"DELETE FROM admin  WHERE Admin_id ='{Admin_id}' "
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return 0
        # rowcount function gives that nothing is updated
        else:
            self.connection.commit()
            return 1


    def close(self):
# Close the cursor and connection when done
      self.cursor.close()
      self.connection.close()


# Create an instance of the MyDatabase class
db = MyDatabase()

# Call the get_users method to retrieve and print data every 4 functions call
# db.delete_user(id="2324")

# Close the database connection when you are done with it
db.close()




