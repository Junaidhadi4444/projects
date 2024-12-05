from flask import Blueprint, request, jsonify
from app.bl.guardian_bl import GuardianBL
from app.schemas.guardian_schema import GuardianSchema, GetGuardianByIdSchema
from marshmallow import ValidationError
from webargs.flaskparser import use_args
from webargs import fields


guardian_bp=Blueprint('guardian_bp', __name__, '/guardians')


# Initialize the Business Logic Layer and Schema
guardian_bl = GuardianBL()
guardian_schema = GuardianSchema()
@guardian_bp.route('', methods=['GET'])
def get_all_guardians():
    guardians = guardian_bl.get_all_guardians()
    return guardian_schema.dump(guardians, many=True), 200

@guardian_bp.route('/guardian', methods=['GET'])
@use_args(GetGuardianByIdSchema(), location="query")
def get_guardian(args):
    guardian_id = args.get('id')
    guardian_data = guardian_bl.get_guardian_by_id(guardian_id)
    if guardian_data:
        return jsonify(guardian_data), 200
    return jsonify({"message": "Guardian not found"}), 404

@guardian_bp.route('', methods=['POST'])
@use_args(GuardianSchema(), location="json")
def create_guardian(args):
    try:
        guardian = guardian_bl.create_guardian(args)
        return guardian_schema.dump(guardian), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400
UpdateGuardianSchema = {
    "id": fields.Int(required=True, error_messages={"required": "Guardian ID is required."}),
    "first_name": fields.Str(required=False, error_messages={"type": "First name must be a string."}),
    "last_name": fields.Str(required=False, error_messages={"type": "Last name must be a string."}),
    "full_name": fields.Str(required=False, error_messages={"type": "Full name must be a string."}),
    "father_name": fields.Str(required=False, error_messages={"type": "Father's name must be a string."}),
    "husband_name": fields.Str(required=False, error_messages={"type": "Husband's name must be a string."}),
    "phone_number": fields.Str(required=False, error_messages={"type": "Phone number must be a string."}),
}

@guardian_bp.route('/guardian', methods=['PUT'])
@use_args(UpdateGuardianSchema, location="json")
def update_guardian(args):
    """
    Update an existing guardian using the provided guardian ID and update data.
    """
    guardian_id = args['id']
    update_data = {key: value for key, value in args.items() if key != "id"}
    try:
        guardian = guardian_bl.update_guardian(guardian_id, update_data)
        if guardian:
            return jsonify(guardian), 200
        else:
            return jsonify({"message": "Guardian not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@guardian_bp.route('/guardian', methods=['DELETE'])
@use_args(GetGuardianByIdSchema(), location="query")
def delete_guardian(args):
    guardian_id = args.get('id')
    guardian = guardian_bl.delete_guardian(guardian_id)
    if guardian:
        return jsonify({"message": "Guardian deleted successfully"}), 200
    return jsonify({"message": "Guardian not found"}), 404