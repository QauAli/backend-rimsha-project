import mysql.connector
import datetime
from flask import jsonify
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
       appointment_dict["Appointment_Date"] = str(row[1])
       appointment_dict["Appointment_Time"] = str(row[2])
       appointment_dict["C_Email_Id"] = row[6]
       appointment_dict["City"] = row[8]
       result.append(appointment_dict)
     return result

    def get_appointment(self, Appointment_id):
        query = f"SELECT * FROM appointment WHERE Appointment_id = '{Appointment_id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            appointment_dict = {}
            appointment_dict["Appointment_id"] = row[0]
            appointment_dict["Appointment_Date"] = row[1]
            appointment_dict["Appointment_Time"] = row[2]
            
        return [appointment_dict]
    

    def get_is_read(self):
     query = "SELECT COUNT(*) FROM appointment WHERE Is_read = '0'"
     self.cursor.execute(query)
     result = self.cursor.fetchone()

     if result is not None:
        new_appointments_count = result[0]
        return {"new_appointments_count": new_appointments_count}
     else:
        return {"new_appointments_count": 0}


    def mark_appointment_as_read(self, Appointment_id, body):
     query = f"UPDATE appointment SET Is_read='1' WHERE Appointment_id='{Appointment_id}'"
     self.cursor.execute(query)

     if self.cursor.rowcount == 0:
        return {"new_appointments_count": 0}
     else:
        self.connection.commit()
        return self.get_is_read()

     
     

        

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



    def get_appointments_in_month(self, year):
        query = (
            "SELECT MONTH(Appointment_Date) AS month, COUNT(*) AS appointment_count "
            "FROM appointment "
            "WHERE YEAR(Appointment_Date) = %s "
            "GROUP BY MONTH(Appointment_Date)"
        )

        try:
            self.cursor.execute(query, (year,))
            results = self.cursor.fetchall()

            # Assuming you want to return the result as JSON
            response = [{'month': int(result[0]), 'appointment_count': int(result[1])} for result in results]
            return response

        except Exception as e:
            error_response = {'error': str(e)}
            return error_response, 500

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




