from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.schemas import UserSchema
from resources.userdb import MyDatabase

blp = Blueprint("user", __name__, description="Operations on user")

@blp.route("/user")
class User(MethodView):
    def __init__(self):
        self.db = MyDatabase()
        # get is used for retriving the specific data
    def getall(self):
     user_id = request.args.get("user_id")


     
     if user_id is None:
      return self.db.get_users()
     else:
      user = self.db.get_user(user_id)
      print(user)
      if user is None:
          abort(404, message="Record doesn't exist")
      return user

    def get(self):
        user_id = request.args.get("user_id")
        if user_id is None:
            return self.db.get_users()
        else:
            user = self.db.get_user(user_id)
            # print(customer)
            if user is None:
                abort(404, message="Record doesn't exist")
            return user

    # post is use for adding the data
    @blp.arguments(UserSchema)
    def post(self,  request_data):
      user_id = request_data.get('user_id')
      self.db.add_user(user_id, request_data)
      return{'message': "user added successfully"}, 201




  # put is used for updating the data
    @blp.arguments(UserSchema)
    def put(self, request_data):
        user_id = request_data.get('user_id')
        print(f"Received request with ID: {user_id}")
        # id = args.get('id')
        if self.db.update_user(user_id, request_data):
            return {'message': "user updated successfully"}, 201
        abort(404, "user not found")




    def delete(self):
        user_id = request.args.get('user_id')  # Use request.args.get to retrieve 'id' from the query parameters

        if self.db.delete_user(user_id):
            return {"message": "user deleted successfully"}
        abort(404, "user not found")
