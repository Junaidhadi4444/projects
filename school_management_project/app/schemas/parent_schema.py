from marshmallow import Schema, fields, validates, ValidationError
from app.models.parent import Parent

class ParentSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    full_name = fields.Str(required=True)
    husband_name = fields.Str()
    role = fields.Str(required=True)
    phone_number = fields.Str(required=True)

    # Nested relationship: List of Students
    students = fields.List(fields.Nested('StudentSchema', only=("id", "full_name")))


    class Meta:
        model = Parent
        load_instance = True
        
class GetParentByIdSchema(Schema):
    id = fields.Int(required=True, error_messages={"required": "Class ID is required."})