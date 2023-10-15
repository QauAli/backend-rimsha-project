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


    def get_users(self):
    #for stoing the json data in the form of list
     result = []
     query = "SELECT * FROM `user`"
# Execute SQL queries or database operations here
     self.cursor.execute(query)

# Fetch and print the results (or iterate through them)
     for row in self.cursor.fetchall():
      #to return the data in the form of json
       user_dict={}
       user_dict["user_id"] = row[0]
       user_dict["username"] = row[1]
       user_dict["email"] = row[2]
       user_dict["password"] = row[3]
       result.append(user_dict)
     return result

    def get_user(self, user_id):
        query = f"SELECT * FROM user WHERE user_id = '{user_id}'"
        self.cursor.execute(query)
        for row in self.cursor.fetchall():
            user_dict = {}
            user_dict["user_id"] = row[0]
            user_dict["username"] = row[1]
            user_dict["email"] = row[2]
            user_dict["password"] = row[3]
        return [user_dict]

    def add_user(self,user_id, body):



        query = f"INSERT INTO user (user_id, username, email, password) VALUES ( '{user_id}','{body['username']}', '{body['email']}', '{body['password']}')"
        self.cursor.execute(query)
        self.connection.commit()

    def update_user(self, user_id, body):
        query = f"UPDATE user SET password='{body['password']}', username='{body['username']}' WHERE user_id='{user_id}'"
        print(query)
        self.cursor.execute(query)
        if self.cursor.rowcount == 0:
            return 0
        else:
            self.connection.commit()
            return 1


    def delete_user(self, user_id):
        query = f"DELETE FROM user  WHERE user_id ='{user_id}' "
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




