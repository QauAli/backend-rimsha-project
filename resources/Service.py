from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.schemas import ServiceSchema
from resources.Servicedb import MyDatabase

blp = Blueprint("service", __name__, description="Operations on service")

@blp.route("/services")
class Service(MethodView):
    def __init__(self):
        self.db = MyDatabase()
        # get is used for retriving the specific data
    def getall(self):
     Service_id = request.args.get("Service_id")
     if Service_id is None:
      return self.db.get_services()
     else:
      service = self.db.get_service(Service_id)
      print(service)
      if service is None:
          abort(404, message="Record doesn't exist")
      return service

    def get(self):
        Service_id = request.args.get("Service_id")
        if Service_id is None:
            return self.db.get_services()
        else:
            service = self.db.get_service(Service_id)
            # print(customer)
            if service is None:
                abort(404, message="Record doesn't exist")
            return service

    # post is use for adding the data
    @blp.arguments(ServiceSchema)
    def post(self,  request_data):
      Service_id = request_data.get('Service_id')
      self.db.add_service(Service_id, request_data)
      return{'message': "service added successfully"}, 201




  # put is used for updating the data
    @blp.arguments(ServiceSchema)
    def put(self, request_data):
        Service_id = request_data.get('Service_id')
        print(f"Received request with ID: {Service_id}")
        # id = args.get('id')
        if self.db.update_service(Service_id, request_data):
            return {'message': "service updated successfully"}, 201
        abort(404, "service not found")



# @blp.route('/service', methods=['DELETE'])

    def delete(self):
        Service_id = request.args.get('Service_id')  # Use request.args.get to retrieve 'id' from the query parameters

        if self.db.delete_service(Service_id):
            return {"message": "service deleted successfully"}
        abort(404, "service not found")
