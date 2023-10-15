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


    def get_services(self):
    #for stoing the json data in the form of list
     result = []
     query = "SELECT * FROM `services`"
# Execute SQL queries or database operations here
     self.cursor.execute(query)

# Fetch and print the results (or iterate through them)
     for row in self.cursor.fetchall():
      #to return the data in the form of json
       service_dict={}
       service_dict["Service_id"] = row[0]
       service_dict["Service_name"] = row[1]
       service_dict["Bill_id"] = row[2]
       service_dict["Staff_id"] = row[3]
       result.append(service_dict)
     return result

    def get_service(self, Service_id):
        query = f"SELECT * FROM services WHERE Service_id = '{Service_id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            service_dict = {}
            service_dict["Service_id"] = row[0]
            service_dict["Service_name"] = row[1]
        return [service_dict]

    def add_service(self,Service_id, body):
        query = f"INSERT INTO services (Service_id, Service_name) VALUES ( '{Service_id}','{body['Service_name']}')"
        self.cursor.execute(query)
        self.connection.commit()

    def update_service(self, Service_id, body):
        query = f"UPDATE services SET Service_name='{body['Service_name']}' WHERE Service_id='{Service_id}'"
        print(query)
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return 0
        else:
            self.connection.commit()
            return 1


    def delete_service(self, Service_id):
        query = f"DELETE FROM services WHERE Service_id ='{Service_id}' "
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

# Call the get_services method to retrieve and print data every 4 functions call
# db.delete_service(id="2324")

# Close the database connection when you are done with it
db.close()




