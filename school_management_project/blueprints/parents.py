from flask import Blueprint, request, jsonify
from app.bl.parent_bl import ParentBL
from app.schemas.parent_schema import ParentSchema, GetParentByIdSchema
from webargs.flaskparser import use_args
from marshmallow import ValidationError
from webargs import fields


parent_bp = Blueprint('parent_bp', __name__, url_prefix='/parents')

# Initialize the Business Logic Layer and Schema
parent_bl = ParentBL()
parent_schema = ParentSchema()
@parent_bp.route('', methods=['GET'])
def get_all_parents():
    parents = parent_bl.get_all_parents()
    return parent_schema.dump(parents, many=True), 200

@parent_bp.route('/parent', methods=['GET'])
@use_args(GetParentByIdSchema(), location="query")
def get_parent(args):
    parent_id = args.get('id')
    parent_data = parent_bl.get_parent_by_id(parent_id)
    if parent_data:
        return jsonify(parent_data), 200
    return jsonify({"message": "Parent not found"}), 404

@parent_bp.route('/parent', methods=['POST'])
@use_args(ParentSchema(), location="json")
def create_parent(args):
    try:
        parent = parent_bl.create_parent(args)
        return parent_schema.dump(parent), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

UpdateParentSchema = {
    "id": fields.Int(required=True, error_messages={"required": "Parent ID is required."}),
    "first_name": fields.Str(required=False, error_messages={"type": "First name must be a string."}),
    "last_name": fields.Str(required=False, error_messages={"type": "Last name must be a string."}),
    "full_name": fields.Str(required=False, error_messages={"type": "Full name must be a string."}),
    "husband_name": fields.Str(required=False, error_messages={"type": "Husband's name must be a string."}),
    "role": fields.Str(required=False, error_messages={"type": "Role must be a string."}),
    "phone_number": fields.Str(required=False, error_messages={"type": "Phone number must be a string."}),
}

@parent_bp.route('/parent', methods=['PUT'])
@use_args(UpdateParentSchema, location="json")
def update_parent(args):
    """
    Update an existing parent using the provided parent ID and update data.
    """
    parent_id = args['id']
    update_data = {key: value for key, value in args.items() if key != "id"}
    try:
        parent = parent_bl.update_parent(parent_id, update_data)
        if parent:
            return jsonify(parent), 200
        else:
            return jsonify({"message": "Parent not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@parent_bp.route('/parent', methods=['DELETE'])
@use_args(GetParentByIdSchema(), location="query")
def delete_parent(args):
    parent_id = args.get('id')
    parent = parent_bl.delete_parent(parent_id)
    if parent:
        return jsonify({"message": "Parent deleted successfully"}), 200
    return jsonify({"message": "Parent not found"}), 404