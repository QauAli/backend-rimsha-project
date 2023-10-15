from marshmallow import Schema, fields
import uuid
# blueprint for StaffSchema data


class StaffSchema(Schema):
    # id = fields.UUID(default=uuid.uuid4, required=True, dump_only=True)
    id = fields.Int(required=True)
    Staff_Name = fields.Str(required=True)
    Staff_Contact = fields.Int(required=True)


class StaffUpdateSchema(Schema):
    id = fields.Int(required=True)
    Staff_Name = fields.Str(required=True)
    Staff_Contact = fields.Int(required=True)


class CustomerSchema(Schema):
    C_Email_Id = fields.Str(required=True)
    C_FirstName = fields.Str(required=True)
    Password = fields.Str(required=True)


class CustomerUpdateSchema(Schema):
    C_Email_Id = fields.Str(required=True)
    C_FirstName = fields.Str(required=True)
    Password = fields.Str(required=True)


class BillSchema(Schema):
    Bill_id = fields.Int(required=True)
    B_amount = fields.Int(required=True)
    Service_id = fields.Int(required=True)
    Customer_id = fields.Int(required=True)


class BillUpdateSchema(Schema):
    Bill_id = fields.Int(required=True)
    B_amount = fields.Int(required=True)


class ServiceSchema(Schema):
    Service_id = fields.Int(required=True)
    Service_name = fields.Str(required=True)


class AppointmentSchema(Schema):
    Appointment_id = fields.Int(required=True)
    Appointment_Date = fields.Date(required=True)
    Appointment_Time = fields.Time(required=True)

class AppointmentAddSchema(Schema):
    Appointment_id = fields.Int(required=True)
    Appointment_Date = fields.Date(required=True)
    Appointment_Time = fields.Time(required=True)
    Name = fields.Str(required=True)
    C_Email_Id = fields.Str(required=True)
    Car_Model_Make = fields.Str(required=True)
    City = fields.Str(required=True)
    ContactNo = fields.Int(required=True)
    Description = fields.Str(required=True)


class AdminSchema(Schema):
    Admin_id  = fields.Int(required=True)
    name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)
    role = fields.Str(required=True)
