from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.schemas import AdminSchema
from resources.Admindb import MyDatabase

blp = Blueprint("admin", __name__, description="Operations on admin")


@blp.route("/admin")
class Admin(MethodView):
    def __init__(self):
        self.db = MyDatabase()
        # get is used for retriving the specific data


    # post is use for adding the data
    @blp.arguments(AdminSchema)
    def post(self, request_data):
        Admin_id  = request_data.get('Admin_id ')
        self.db.add_admin(Admin_id , request_data)
        return {'message': "admin added successfully"}, 201

    # put is used for updating the data
    @blp.arguments(AdminSchema)
    def put(self, request_data):
        Admin_id  = request_data.get('Admin_id ')
        print(f"Received request with ID: {Admin_id}")
        # id = args.get('id')
        if self.db.update_admin(Admin_id , request_data):
            return {'message': "admin updated successfully"}, 201
        abort(404, "admin not found")

    def delete(self):
        Admin_id  = request.args.get('Admin_id ')  # Use request.args.get to retrieve 'id' from the query parameters

        if self.db.delete_admin(Admin_id ):
            return {"message": "admin deleted successfully"}
        abort(404, "admin not found")
