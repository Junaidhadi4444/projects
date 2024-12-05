from flask import Blueprint, request, jsonify
from app.bl.student_bl import StudentBL
from app.schemas.student_schema import StudentSchema, GetStudentByIdSchema
from webargs.flaskparser import use_args
from webargs import fields
from marshmallow import ValidationError

student_bp = Blueprint('student_bp', __name__, url_prefix='/students')

# Initialize the Business Logic Layer and Schema
student_bl = StudentBL()
student_schema = StudentSchema()


@student_bp.route('/students', methods=['GET'])
def get_all_students():
    students = student_bl.get_all_students()
    return student_schema.dump(students, many=True), 200

@student_bp.route('/student', methods=['GET'])
@use_args(GetStudentByIdSchema(), location="query")
def get_student(args):
    student_id = args.get('id')
    student_data = student_bl.get_student_by_id(student_id)
    if student_data:
        return jsonify(student_data), 200
    return jsonify({"message": "Student not found"}), 404

@student_bp.route('/student', methods=['POST'])
@use_args(StudentSchema(), location="json")
def create_student(args):
    try:
        student = student_bl.create_student(args)
        return student_schema.dump(student), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

UpdateStudentSchema = {
    "id": fields.Int(required=True, error_messages={"required": "Student ID is required."}),
    "first_name": fields.Str(required=False, error_messages={"type": "First name must be a string."}),
    "last_name": fields.Str(required=False, error_messages={"type": "Last name must be a string."}),
    "full_name": fields.Str(required=False, error_messages={"type": "Full name must be a string."}),
    "father_name": fields.Str(required=False, error_messages={"type": "Father's name must be a string."}),
    "guardian_name": fields.Str(required=False, error_messages={"type": "Guardian's name must be a string."}),
    "status": fields.Str(required=False, error_messages={"type": "Status must be a string."}),
    "class_id": fields.Int(required=False, error_messages={"type": "Class ID must be an integer."}),
}
@student_bp.route('/student', methods=['PUT'])
@use_args(UpdateStudentSchema, location="json")
def update_student(args):
    """
    Update an existing student using the provided student ID and update data.
    """
    student_id = args['id']
    update_data = {key: value for key, value in args.items() if key != "id"}
    try:
        student = student_bl.update_student(student_id, update_data)
        if student:
            return jsonify({"message": "Student updated successfully"}), 200
        else:
            return jsonify({"message": "Student not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500
    
@student_bp.route('/student', methods=['DELETE'])
@use_args(GetStudentByIdSchema(), location="query")
def delete_student(args):
    student_id = args.get('id')
    student = student_bl.delete_student(student_id)
    if student:
        return jsonify({"message": "Student deleted successfully"}), 200
    return jsonify({"message": "Student not found"}), 404