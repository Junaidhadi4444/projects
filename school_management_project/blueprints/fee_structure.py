from flask import Blueprint, request, jsonify
from app.bl.fee_structure_bl import FeeStructureBL
from app.schemas.fee_structure_schema import FeeStructureSchema, GetFeeStructureByIdSchema
from webargs.flaskparser import use_args
from marshmallow import ValidationError
from webargs import fields

fee_structure_bp = Blueprint('fee_structure_bp', __name__, '/fee_structure')

# Initialize the Business Logic Layer and Schema
fee_structure_bl = FeeStructureBL()
fee_structure_schema = FeeStructureSchema()
@fee_structure_bp.route('', methods=['GET'])
def get_all_fee_structures():
    fee_structures = fee_structure_bl.get_all_fee_structures()
    return jsonify(fee_structure_schema.dump(fee_structures, many=True)), 200

# Route to get a fee structure by ID
@fee_structure_bp.route('/fee_structure', methods=['GET'])
@use_args(GetFeeStructureByIdSchema(), location="query")
def get_fee_structure(args):
    fee_structure_id = args.get('id')
    fee_structure_data = fee_structure_bl.get_fee_structure_by_id(fee_structure_id)
    if fee_structure_data:
        return jsonify(fee_structure_data), 200
    return jsonify({"message": "Fee structure not found"}), 404

# Route to create a fee structure
@fee_structure_bp.route('/fee_structure', methods=['POST'])
@use_args(FeeStructureSchema(), location="json")
def create_fee_structure(args: dict):
    """
    Create a new fee structure using the provided data.
    """
    try:
        fee_structure = fee_structure_bl.create_fee_structure(args)
        return fee_structure_schema.dump(fee_structure), 201
    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

# Define the schema for updating a fee structure
UpdateFeeStructureSchema = {
    "id": fields.Int(required=True, error_messages={"required": "Fee structure ID is required."}),
    "fee": fields.Float(required=False, error_messages={"type": "Fee must be a float."}),
    "dues": fields.Float(required=False, error_messages={"type": "Dues must be a float."}),
    "discount": fields.Float(required=False, error_messages={"type": "Discount must be a float."}),
}

# Route to update a fee structure
@fee_structure_bp.route('/fee_structure', methods=['PUT'])
@use_args(UpdateFeeStructureSchema, location="json")
def update_fee_structure(args: dict):
    fee_structure_id = args['id']
    update_data = {key: value for key, value in args.items() if key != "id"}
    try:
        response, status_code = fee_structure_bl.update_fee_structure(fee_structure_id, update_data)
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# Route to delete a fee structure
@fee_structure_bp.route('/fee_structure', methods=['DELETE'])
@use_args(GetFeeStructureByIdSchema(), location="query")
def delete_fee_structure(args: dict):
    """
    Delete a fee structure by ID passed in the query string.
    """
    try:
        fee_structure_id = args['id']
        fee_structure = fee_structure_bl.delete_fee_structure(fee_structure_id)
        if fee_structure:
            return jsonify({"message": "Fee structure deleted successfully"}), 200
        return jsonify({"message": "Fee structure not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500