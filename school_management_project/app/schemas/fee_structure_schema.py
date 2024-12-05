from marshmallow import Schema, fields
from app.models.fee_structure import FeeStructure


class FeeStructureSchema(Schema):
    id = fields.Int(dump_only=True)
    fee = fields.Float(required=True)
    dues = fields.Float(required=True)
    discount = fields.Float()

    class Meta:
        model = FeeStructure
        load_instance = True

class GetFeeStructureByIdSchema(Schema):
    id = fields.Int(required=True, error_messages={"required": "Class ID is required."})
