from flask import Blueprint, jsonify
from app.bl.class_bl import ClassBL
from app.schemas.class_schema import ClassSchema, GetClassByIdSchema
from webargs.flaskparser import use_args
from webargs import fields
from marshmallow import ValidationError

class_bp = Blueprint('class_bp', __name__, url_prefix='/classes')

class_bl = ClassBL()
class_schema = ClassSchema()

# use web args or marshmallow 
@class_bp.route('', methods=['GET'])
def get_all_classes():
    classes = class_bl.get_all_classes()
    return jsonify(class_schema.dump(classes, many=True)), 200

@class_bp.route('/class', methods=['GET'])
@use_args(GetClassByIdSchema(), location="query")
def get_class(args):
    class_id = args.get('id')
    class_data = class_bl.get_class_by_id(class_id)
    if class_data:
        return jsonify(class_data), 200
    return jsonify({"message": "Class not found"}), 404


@class_bp.route('/class', methods=['POST'])
@use_args(ClassSchema(), location="json") 
def create_class(args: dict):
    """
    Create a new class using the provided data.
    """
    try:
        # args now contains the validated data
        class_ = class_bl.create_class(args)  
        return class_schema.dump(class_), 201
    except ValidationError as e:  
        return jsonify({"error": str(e)}), 400

UpdateClassSchema = {
    "id": fields.Int(required=True, error_messages={"required": "Class ID is required."}),
    "class_name": fields.Str(required=False, error_messages={"type": "Class name must be a string."}),
    "section": fields.Str(required=False, error_messages={"type": "Section must be a string."}),
    "teacher_id": fields.Int(required=False, error_messages={"type": "Teacher ID must be an integer."}),
}

@class_bp.route('/class', methods=['PUT'])
@use_args(UpdateClassSchema, location="json")
def update_class(args: dict):
    """
    Update an existing class using the provided class ID and update data.
    """
    class_id = args['id']
    update_data = {key: value for key, value in args.items() if key != "id"}
    try:
        response = class_bl.update_class(class_id, update_data)
        if response:
            return jsonify(response), 200
        else:
            return jsonify({"message": "Class not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@class_bp.route('/class', methods=['DELETE'])
@use_args(GetClassByIdSchema(), location="query")
def delete_class(args: dict):
    """
    Delete a class by ID passed in the query string.
    """
    try:
        class_id = args['id'] 
        class_ = class_bl.delete_class(class_id)
        if class_:
            return jsonify({"message": "Class deleted successfully"}), 200
        return jsonify({"message": "Class not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500