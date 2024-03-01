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

    def add_customer(self,  C_FirstName, C_Email_Id, Password):
        query = f"INSERT INTO customer (C_FirstName, C_Email_Id, Password,) VALUES ('{C_FirstName}','{C_Email_Id}', '{Password}')"
        self.cursor.execute(query)
        self.connection.commit()



    def update_feedback(self, C_Email_Id, Feedback):
        try:
            query = f"UPDATE customer SET Feedback='{Feedback}' WHERE C_Email_Id='{C_Email_Id}'"
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"Error adding feedback: {str(e)}")
            self.connection.rollback()


    def check_customer(self, C_Email_Id):
        query = f"SELECT * FROM customer WHERE C_Email_Id = '{C_Email_Id}'"
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result is not None

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

     if row is not None:
        user_dict = {
            "email": row[0],
            "password": row[1],
            "role": row[2]
        }
        return user_dict
     else:
        return None
     


    def upload_profile_image(self, email, file_path, role):
    # Update the table associated with the user's role
     if role == 'admin':
        table_name = 'admin'
        email_column = 'email'
     elif role == 'customer':
        table_name = 'customer'
        email_column = 'C_Email_Id'
     elif role == 'staff':
        table_name = 'staff'
        email_column = 'email'
     else:
        # Handle unsupported roles
        return False

    # Insert the image path into the corresponding table
     query = f"""
        UPDATE {table_name} SET Image = '{file_path}' WHERE {email_column} = '{email}';
    """

     try:
        self.cursor.execute(query)
        self.connection.commit()
        return True
     except Exception as e:
        print(f"Error uploading profile image: {e}")
        self.connection.rollback()
        return False

     
    
    def update_profile(self, body):
    # Extract relevant information
     name = body.get("name")
     password = body.get("password")
     newpassword = body.get("newpassword")
     email = body.get("email")

    # Validate that at least one of the fields is present
     if name is None and password is None and email is None:
        return 0

    # Determine the table and update fields based on the user's role obtained during login
     role = self.get_user_role(email, password)
     print("entered role is" +  str(role))
     print("")

     if role == 'admin':
        query = f"""
            UPDATE admin SET name='{name}', password='{newpassword}' WHERE email = '{email}' AND password = '{password}'
        """
     elif role == 'customer':
        query = f"""
            UPDATE customer SET C_FirstName='{name}', Password='{newpassword}' WHERE C_Email_id = '{email}' AND Password = '{password}'
        """
     elif role == 'staff':
        query = f"""
            UPDATE staff SET staff_Name='{name}', password='{newpassword}' WHERE email = '{email}' AND password = '{password}'
        """
     else:
        return 0
     
    # Execute the query
     self.cursor.execute(query)
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
db.close()




