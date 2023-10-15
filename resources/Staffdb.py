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


    def get_allstaff(self):
    #for stoing the json data in the form of list
     result = []
     query = "SELECT * FROM `staff`"
# Execute SQL queries or database operations here
     self.cursor.execute(query)

# Fetch and print the results (or iterate through them)
     for row in self.cursor.fetchall():
      #to return the data in the form of json
       staff_dict={}
       staff_dict["id"] = row[0]
       staff_dict["Staff_Name"] = row[1]
       staff_dict["Staff_Contact"] = row[2]
       staff_dict["Staff_Designation"] = row[3]
       staff_dict["Customer_id"] = row[4]
       staff_dict["Appoitment_id"] = row[5]
       staff_dict["Bill-id"] = row[6]
       result.append(staff_dict)
     return result

    def get_staff(self, id):
        query = f"SELECT * FROM staff WHERE id = '{id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            customer_dict = {}
            staff_dict = {}
            staff_dict["id"] = row[0]
            staff_dict["Staff_Name"] = row[1]
            staff_dict["Staff_Contact"] = row[2]
        return[staff_dict]

    def add_staff(self,id, body):
        query = f"INSERT INTO staff (id, Staff_Name, Staff_Contact) VALUES ( '{id}','{body['Staff_Name']}','{body['Staff_Contact']}')"
        self.cursor.execute(query)
        self.connection.commit()

    def update_staff(self, id, body):
        query = f"UPDATE staff SET Staff_Name='{body['Staff_Name']}', Staff_Contact='{body['Staff_Contact']}' WHERE id='{id}'"
        print(query)
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return 0
        else:
            self.connection.commit()
            return 1


    def delete_staff(self, id):
        query = f"DELETE FROM staff WHERE id ='{id}' "
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

# Call the get_staffs method to retrieve and print data every 4 functions call
# db.delete_staff(id="2324")

# Close the database connection when you are done with it
db.close()




