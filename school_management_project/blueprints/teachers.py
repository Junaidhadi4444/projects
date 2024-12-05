from flask import Blueprint, request, jsonify
from app.bl.teacher_bl import TeacherBL
from app.schemas.teacher_schema import TeacherSchema, GetTeacherByIdSchema, UpdateTeacherSchema
from webargs.flaskparser import use_args
from marshmallow import ValidationError
from webargs import fields

teacher_bp = Blueprint('teacher_bp', __name__, url_prefix='/teachers')

# Initialize the Business Logic Layer and Schema
teacher_bl = TeacherBL()
teacher_schema = TeacherSchema()

@teacher_bp.route('/teachers', methods=['GET'])
def get_all_teachers():
    teachers = teacher_bl.get_all_teachers()
    return teacher_schema.dump(teachers, many=True), 200

@teacher_bp.route('/teacher', methods=['GET'])
@use_args(GetTeacherByIdSchema(), location="query")
def get_teacher(args):
    teacher_id = args.get('id')
    teacher_data = teacher_bl.get_teacher_by_id(teacher_id)
    if teacher_data:
        return jsonify(teacher_data), 200
    return jsonify({"message": "Teacher not found"}), 404

@teacher_bp.route('/teacher', methods=['POST'])
@use_args(TeacherSchema(), location="json")
def create_teacher(args):
    try:
        teacher = teacher_bl.create_teacher(args)
        return jsonify({
            "message": "Teacher created successfully",
            "data": teacher_schema.dump(teacher)
        }), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400


@teacher_bp.route('/teacher', methods=['PUT'])
@use_args(UpdateTeacherSchema, location="json")
def update_teacher(args):
    """
    Update an existing teacher using the provided teacher ID and update data.
    """
    teacher_id = args['id']
    update_data = {key: value for key, value in args.items() if key != "id"}
    try:
        teacher = teacher_bl.update_teacher(teacher_id, update_data)
        if teacher:
            return jsonify(teacher), 200
        else:
            return jsonify({"message": "Teacher not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@teacher_bp.route('/teacher', methods=['DELETE'])
@use_args(GetTeacherByIdSchema(), location="query")
def delete_teacher(args):
    teacher_id = args.get('id')

    if not teacher_id:
        return jsonify({"message": "Teacher ID is required"}), 400
    is_deleted = teacher_bl.delete_teacher(teacher_id)
    if is_deleted:
        return jsonify({"message": "Teacher deleted successfully"}), 200
    return jsonify({"message": "Teacher not found"}), 404

