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


    def get_customers(self):
    #for stoing the json data in the form of list
     result = []
     query = "SELECT * FROM `customer`"
# Execute SQL queries or database operations here
     self.cursor.execute(query)

# Fetch and print the results (or iterate through them)
     for row in self.cursor.fetchall():
      #to return the data in the form of json
       customer_dict={}
       customer_dict["Customer_id"] = row[1]
       customer_dict["C_FirstName"] = row[2]
       customer_dict["C_LastName"] = row[3]
       customer_dict["C_Phoneno"] = row[4]
       customer_dict["C_Address"] = row[5]
       customer_dict["C_Email_Id"] = row[6]
       customer_dict["Password"] = row[7]
       customer_dict["C_Bill-id"] = row[8]
       customer_dict["C_Appointment-id"] = row[9]
       customer_dict["C_Service-name"] = row[10]
       result.append(customer_dict)
     return result

    def get_customer(self, Customer_id):
        query = f"SELECT * FROM customer WHERE Customer_id = '{Customer_id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            customer_dict = {}
            customer_dict["Customer_id"] = row[1]
            customer_dict["C_FirstName"] = row[2]
            customer_dict["C_LastName"] = row[3]
            customer_dict["C_Email_Id"] = row[6]
            customer_dict["Password"] = row[7]
        return [customer_dict]

    def add_customer(self, C_Email_Id, Password, C_FirstName):
        query = f"INSERT INTO customer (C_Email_Id, Password, C_FirstName) VALUES ('{C_Email_Id}', '{Password}', '{C_FirstName}')"
        self.cursor.execute(query)
        self.connection.commit()

    def customer_exists(self, C_Email_Id, C_FirstName):
        query = f"SELECT * FROM customer WHERE C_Email_Id = '{C_Email_Id}' AND C_FirstName = '{C_FirstName}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result is not None  # Return True if a customer with the same email and first name exists, False otherwise

    def update_customer(self, C_Email_Id, body):
        query = f"UPDATE customer SET C_FirstName='{body['C_FirstName']}', Password='{body['Password']}' WHERE C_Email_Id='{C_Email_Id}'"
        # print(query)
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return 0
        else:
            self.connection.commit()
            return 1
        

    def get_total_customers(self):
        query = "SELECT COUNT(*) FROM customer"
        self.cursor.execute(query)
    
    # Fetch the count value
        total_customers = self.cursor.fetchone()[0]
        return total_customers

        

    def delete_customer(self, Customer_id):
        query = f"DELETE FROM customer WHERE Customer_id ='{Customer_id}' "
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return 0
        # rowcount function gives that nothing is updated
        else:
            self.connection.commit()
            return 1
        


    def verify_user(self, email, password, role):
     query = f"""
        SELECT email, password, 'admin' as role FROM admin WHERE email = '{email}' AND password = '{password}' 
        UNION
        SELECT C_Email_Id as email, Password as password, 'customer' as role FROM customer WHERE C_Email_Id = '{email}' AND Password = '{password}' 
        UNION
        SELECT email, password, 'staff' as role FROM staff WHERE email = '{email}' AND password = '{password}';
        """

     self.cursor.execute(query)
     row = self.cursor.fetchone()
   
     user_dict={}
     user_dict["email"] = row[0]
     user_dict["password"] = row[1]
     user_dict["role"] = row[2]
    
     return user_dict
    

    def update_profile(self, id, body):
    
    # Extract relevant information
     name = body.get("name")
     password = body.get("password")
     email = body.get("email")
     print("name" + name)
     print(f"Type of 'name': {type(name)}")
     print(f"Value of 'name': {name}")


    # Validate that at least one of the fields is present
     if name is None and password is None and email is None:
        return 0

    # Determine the table and update fields based on the user's role obtained during login
     role = self.get_user_role(email, password)
     print("entered role is" +  str(role))

     if role == 'admin':
        query = f"""
            UPDATE admin SET name='{name}', password='{password}', email='{email}' WHERE Admin_id = {id}
        """
     elif role == 'customer':
          query = f"""
            UPDATE customer SET C_FirstName='{name}', Password='{password}', C_Email_Id='{email}' WHERE Customer_id = {id}
        """
     elif role == 'staff':
          query = f"""
            UPDATE staff SET staff_Name='{name}', password='{password}', email='{email}' WHERE id = {id}
        """
     else:
        return 0

    # Execute the query
     self.cursor.execute(query)
     print(f"Email in get_user_role: {email}")
     print(f"Password in get_user_role: {password}")


    # Check for a successful update
     if self.cursor.rowcount == 0:
        return 0
     else:
        self.connection.commit()
        return 1

    def get_user_role(self, email, password):
     query = f"""
        SELECT 'admin' as role FROM admin WHERE email = '{email}' AND password = '{password}'
        UNION
        SELECT 'customer' as role FROM customer WHERE C_Email_Id = '{email}' AND Password = '{password}'
        UNION
        SELECT 'staff' as role FROM staff WHERE email = '{email}' AND password = '{password}'
    """

     self.cursor.execute(query)
     print(f"SQL Query: {query}")

     row = self.cursor.fetchone()

     if row is not None:
      return row[0]
     else:
      return None



    

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




