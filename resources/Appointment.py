from flask import request
from datetime import datetime, timedelta
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from resources.schemas import AppointmentSchema
from resources.schemas import AppointmentAddSchema
from resources.schemas import MarkRead
from resources.schemas import BillInMonth
from resources.Appointmentdb import MyDatabase

blp = Blueprint("appointment", __name__, description="Operations on appointment")
new_appointment_count = 0

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




    def delete(self):
        Appointment_id = request.args.get('Appointment_id')  # Use request.args.get to retrieve 'id' from the query parameters

        if self.db.delete_appointment(Appointment_id):
            return {"message": "appointment deleted successfully"}
        abort(404, "appointment not found")



@blp.route("/unread_appointments")
class TotalAppointments(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    def get(self):
        new_appointments = self.db.get_is_read()
        response = {"new_appointments": new_appointments}
        return response


@blp.route("/mark_read")
class MarkReadAppointment(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    @blp.arguments(MarkRead)
    def put(self, request_data):
        Appointment_id = request_data.get('Appointment_id')
        print(f"Received request to mark as read: {Appointment_id}")

        # Update the Is_read column in the database
        if self.db.mark_appointment_as_read(Appointment_id,request_data):
            return {"message": "Appointment marked as read successfully"},201
        abort(404, "Appointment not found")


@blp.route("/total_appointments_in_month")
class AppointmentsInMonth(MethodView):
    def __init__(self):
        self.db = MyDatabase()

    @blp.arguments(BillInMonth)
    def post(self, request_data):
        year = request_data.get('year')
        total_appointments_in_month = self.db.get_appointments_in_month(year)
        return {"total_appointments_in_month": total_appointments_in_month}