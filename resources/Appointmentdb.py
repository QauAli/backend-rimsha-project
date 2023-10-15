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


    def get_appointments(self):
    #for stoing the json data in the form of list
     result = []
     query = "SELECT * FROM `appointment`"
# Execute SQL queries or database operations here
     self.cursor.execute(query)

# Fetch and print the results (or iterate through them)
     for row in self.cursor.fetchall():
      #to return the data in the form of json
       appointment_dict={}
       appointment_dict["Appointment_id"] = row[0]
       appointment_dict["Appointment_Date"] = row[1]
       appointment_dict["Appointment_Time"] = row[2]
       appointment_dict["Staff_id"] = row[3]
       appointment_dict["Customer_id"] = row[4]
       result.append(appointment_dict)
     return result

    def get_appointment(self, Appointment_id):
        query = f"SELECT * FROM appointment WHERE Appointment_id = '{Appointment_id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            appointment_dict = {}
            appointment_dict["Appointment_id"] = row[1]
            appointment_dict["Appointment_Date"] = row[2]
            appointment_dict["Appointment_Time"] = row[3]
        return [appointment_dict]

    def add_appointment(self,Appointment_id, body):
        query = f"INSERT INTO appointment (Appointment_id, Appointment_Date, Appointment_Time,Name,C_Email_Id,Car_Model_Make,City,ContactNo,Description) VALUES ( '{Appointment_id}','{body['Appointment_Date']}', '{body['Appointment_Time']}','{body['Name']}','{body['C_Email_Id']}','{body['Car_Model_Make']}','{body['City']}','{body['ContactNo']}','{body['Description']}')"
        self.cursor.execute(query)
        self.connection.commit()

    def update_appointment(self, Appointment_id, body):
        query = f"UPDATE appointment SET Appointment_Date='{body['Appointment_Date']}', Appointment_Time='{body['Appointment_Time']}' WHERE Appointment_id='{Appointment_id}'"
        print(query)
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return 0
        else:
            self.connection.commit()
            return 1


    def delete_appointment(self, Appointment_id):
        query = f"DELETE FROM appointment WHERE Appointment_id ='{Appointment_id}' "
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

# Call the get_appointments method to retrieve and print data every 4 functions call
# db.delete_appointment(id="2324")

# Close the database connection when you are done with it
db.close()




