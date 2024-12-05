from marshmallow import Schema, fields, validates, ValidationError
from app.models.student import Student

class StudentSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    full_name = fields.Str(required=True)
    father_name = fields.Str(required=True)
    guardian_name = fields.Str()
    status = fields.Str(required=True)

    class_id = fields.Int(required=True)

    # Nested relationship: List of Parents
    parents = fields.List(fields.Nested('ParentSchema', only=("id", "full_name")))

    class Meta:
        model = Student
        load_instance = True
        
class GetStudentByIdSchema(Schema):
    id = fields.Int(required=True, error_messages={"required": "Class ID is required."})
