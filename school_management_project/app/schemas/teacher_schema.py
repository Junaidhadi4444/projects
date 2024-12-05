from marshmallow import Schema, fields, validates, ValidationError
from app.models.teacher import Teacher
from app.schemas.class_schema import ClassSchema

class TeacherSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    full_name = fields.Str(required=True)
    father_name = fields.Str(required=True)
    status = fields.Str(required=True)
    subject = fields.Str(required=True)
    qualification = fields.Str(required=True)
    email = fields.Email(required=True)

    # One-to-Many relationship: A teacher can have multiple classes
    classes = fields.Nested(ClassSchema, many=True, dump_only=True)

    @validates('email')
    def validate_email(self, value):
        if '@' not in value:
            raise ValidationError("Invalid email address.")

    class Meta:
        model = Teacher
        load_instance = True

class GetTeacherByIdSchema(Schema):
    id = fields.Int(required=True, error_messages={"required": "Class ID is required."})

from marshmallow import Schema, fields

class UpdateTeacherSchema(Schema):
    id = fields.Int(required=True, error_messages={"required": "Teacher ID is required."})
    first_name = fields.Str(required=False, error_messages={"type": "First name must be a string."})
    last_name = fields.Str(required=False, error_messages={"type": "Last name must be a string."})
    full_name = fields.Str(required=False, error_messages={"type": "Full name must be a string."})
    father_name = fields.Str(required=False, error_messages={"type": "Father's name must be a string."})
    status = fields.Str(required=False, error_messages={"type": "Status must be a string."})
    subject = fields.Str(required=False, error_messages={"type": "Subject must be a string."})
    qualification = fields.Str(required=False, error_messages={"type": "Qualification must be a string."})
    email = fields.Email(required=False, error_messages={"type": "Email must be valid."})
