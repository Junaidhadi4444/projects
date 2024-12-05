from app.repo.fee_structure_repo import FeeStructureRepository
from app.models.fee_structure import FeeStructure
from app.schemas.fee_structure_schema import FeeStructureSchema
from marshmallow import ValidationError

class FeeStructureBL:
    # Method to get all fee structures
    @staticmethod
    def get_all_fee_structures():
        fee_structure=FeeStructureRepository.get_all_fee_structures()
        return fee_structure
    
    # Method to get a fee structure by its ID
    @staticmethod
    def get_fee_structure_by_id(fee_structure_id):
        fee_structure = FeeStructureRepository.get_fee_structure(fee_structure_id)  
        if fee_structure:
            fee_structure_schema = FeeStructureSchema()
            return fee_structure_schema.dump(fee_structure), 200
        return {"message": "Fee structure not found"}, 404
    
    # Method to create a new fee structure
    @staticmethod
    def create_fee_structure(data):
        try:
            # Validate and deserialize data
            fee_structure_schema = FeeStructureSchema()  
            fee_structure_data = fee_structure_schema.load(data)
            # Create a new fee structure using deserialized data (not an instance)
            new_fee_structure = FeeStructure(**fee_structure_data)  # Using the deserialized data
            FeeStructureRepository.create_fee_structure(new_fee_structure)
            return fee_structure_schema.dump(new_fee_structure), 201
        except ValidationError as e:
            return {"error": str(e)}, 400
        
    @staticmethod
    def update_fee_structure(fee_structure_id, data):
        """
        Update a fee structure using its ID and the provided data.
        """
        # Retrieve the fee structure object from the repository
        fee_structure = FeeStructureRepository.get_fee_structure(fee_structure_id)
        if not fee_structure:
            return {"message": "Fee structure not found"}, 404
        
        try:
            # Validate and deserialize the input data
            fee_structure_schema = FeeStructureSchema()
            updated_data = fee_structure_schema.load(data, partial=True)
            
            for key, value in updated_data.items():
                setattr(fee_structure, key, value)

            FeeStructureRepository.update_fee_structure(fee_structure)
            
            return fee_structure_schema.dump(fee_structure), 200
        
        except ValidationError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500


    # Method to delete a fee structure
    @staticmethod
    def delete_fee_structure(fee_structure_id):
        fee_structure = FeeStructureRepository.get_fee_structure(fee_structure_id)
        if fee_structure:
            FeeStructureRepository.delete_fee_structure(fee_structure)  # Correct method call
            return {"message": "Fee structure deleted"}, 200
        return {"message": "Fee structure not found"}, 404
