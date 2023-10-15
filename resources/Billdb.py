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


    def get_bills(self):
    #for stoing the json data in the form of list
     result = []
     query = "SELECT * FROM `bills`"
# Execute SQL queries or database operations here
     self.cursor.execute(query)

# Fetch and print the results (or iterate through them)
     for row in self.cursor.fetchall():
      #to return the data in the form of json
       bill_dict={}
       bill_dict["Bill_id"] = row[0]
       bill_dict["B_amount"] = row[1]
       bill_dict["Service_id"] = row[2]
       bill_dict["Customer_id"] = row[3]
       result.append(bill_dict)
     return result

    def get_bill(self, Bill_id):
        query = f"SELECT * FROM bills WHERE Bill_id = '{Bill_id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            bill_dict = {}
            bill_dict["Bill_id"] = row[0]
            bill_dict["B_amount"] = row[1]
            bill_dict["Service_id"] = row[2]
            bill_dict["Customer_id"] = row[3]
        return [bill_dict]

    def add_bill(self,Bill_id, body):
        query = f"INSERT INTO bills (Bill_id, B_amount, Service_id, Customer_id) VALUES ( '{Bill_id}','{body['B_amount']}', '{body['Service_id']}','{body['Customer_id']}')"
        self.cursor.execute(query)
        self.connection.commit()

    def update_bill(self, Bill_id, body):
        query = f"UPDATE bills SET B_amount='{body['B_amount']}' WHERE Bill_id='{Bill_id}'"
        print(query)
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return 0
        else:
            self.connection.commit()
            return 1


    def delete_bill(self, Bill_id):
        query = f"DELETE FROM bills WHERE Bill_id ='{Bill_id}' "
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

# Call the get_items method to retrieve and print data every 4 functions call
# db.delete_item(id="2324")

# Close the database connection when you are done with it
db.close()




