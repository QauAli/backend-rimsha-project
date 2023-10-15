from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.schemas import AppointmentSchema
from resources.schemas import AppointmentAddSchema
from resources.Appointmentdb import MyDatabase

blp = Blueprint("appointment", __name__, description="Operations on appointment")

@blp.route("/appointment")
class Appointment(MethodView):
    def __init__(self):
        self.db = MyDatabase()
        # get is used for retriving the specific data
    def getall(self):
     Appointment_id = request.args.get("Appointment_id")
     if Appointment_id is None:
      return self.db.get_appointments()
     else:
      appointment = self.db.get_appointment(Appointment_id)
      print(appointment)
      if appointment is None:
          abort(404, message="Record doesn't exist")
      return appointment

    def get(self):
        Appointment_id = request.args.get("Appointment_id")
        if Appointment_id is None:
            return self.db.get_appointments()
        else:
            appointment = self.db.get_appointment(Appointment_id)
            # print(customer)
            if appointment is None:
                abort(404, message="Record doesn't exist")
            return appointment

    # post is use for adding the data
    @blp.arguments(AppointmentAddSchema)
    def post(self,  request_data):
      Appointment_id = request_data.get('Appointment_id')
      self.db.add_appointment(Appointment_id, request_data)
      return{'message': "Appointment added successfully"}, 201




  # put is used for updating the data
    @blp.arguments(AppointmentSchema)
    def put(self, request_data):
        Appointment_id = request_data.get('Appointment_id')
        print(f"Received request with ID: {Appointment_id}")
        # id = args.get('id')
        if self.db.update_appointment(Appointment_id, request_data):
            return {'message': "appointment updated successfully"}, 201
        abort(404, "appointment not found")



# @blp.route('/appointment', methods=['DELETE'])

    def delete(self):
        Appointment_id = request.args.get('Appointment_id')  # Use request.args.get to retrieve 'id' from the query parameters

        if self.db.delete_appointment(Appointment_id):
            return {"message": "appointment deleted successfully"}
        abort(404, "appointment not found")
