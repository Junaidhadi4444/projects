from marshmallow import Schema, fields, validate
from app.models.classs import Class
from app.schemas.student_schema import StudentSchema

class ClassSchema(Schema):
    id = fields.Int(dump_only=True)
    class_name = fields.Str(required=True)
    section = fields.Str(required=True)
    teacher_id = fields.Int(required=True)

    students = fields.Nested(StudentSchema, many=True, dump_only=True)

    class Meta:
        model = Class
        load_instance = True

class GetClassByIdSchema(Schema):
    id = fields.Int(required=True, error_messages={"required": "Class ID is required."})






