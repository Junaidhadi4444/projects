from marshmallow import Schema, fields, validates, ValidationError
from app.models.guardian import Guardian

class GuardianSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    full_name = fields.Str(required=True)
    father_name = fields.Str()
    husband_name = fields.Str()
    phone_number = fields.Str(required=True)

    class Meta:
        model = Guardian
        load_instance = True

class GetGuardianByIdSchema(Schema):
    id = fields.Int(required=True, error_messages={"required": "Class ID is required."})