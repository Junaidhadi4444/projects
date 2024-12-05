from app.repo.guardian_repo import GuardianRepository
from app.models.guardian import Guardian
from app.schemas.guardian_schema import GuardianSchema
from marshmallow import ValidationError

class GuardianBL:
    @staticmethod
    def get_all_guardians():
        guardains=GuardianRepository.get_all_guardians()
        return guardains
    
    @staticmethod
    def get_guardian_by_id(guardian_id):
        guardian = GuardianRepository.get_guardian(guardian_id)
        if guardian:
            guardian_schema = GuardianSchema()
            return guardian_schema.dump(guardian), 200
        return {"message": "Guardian not found"}, 404
    
    @staticmethod
    def create_guardian(data):
        try:
            # Validate and deserialize data
            guardian_schema = GuardianSchema()
            guardian_data = guardian_schema.load(data)  # This is a dictionary now, not a Guardian object

            # Create a new guardian
            guardian = Guardian(**guardian_data)  # Create the Guardian object with the dict data
            GuardianRepository.create_guardian(guardian_data)  # Pass the dict, not the Guardian object
            return guardian_schema.dump(guardian), 201
        except ValidationError as e:
            return {"error": str(e)}, 400

    @staticmethod
    def update_guardian(guardian_id, data):
        guardian = GuardianRepository.get_guardian(guardian_id)
        if guardian:
            try:
                # Validate and deserialize the incoming data
                guardian_schema = GuardianSchema()
                updated_data = guardian_schema.load(data, partial=True)  # Partial load to allow partial updates
                
                # Update the guardian's attributes manually
                for key, value in updated_data.items():
                    setattr(guardian, key, value)

                GuardianRepository.update_guardian(guardian)

                # Return the updated guardian's data
                return guardian_schema.dump(guardian), 200
            except ValidationError as e:
                return {"error": str(e)}, 400
        return {"message": "Guardian not found"}, 404

    @staticmethod
    def delete_guardian(guardian_id):
        guardian = GuardianRepository.get_guardian(guardian_id)
        if guardian:
            GuardianRepository.delete_guardian(guardian)
            return {"message": "Guardian deleted"}, 200
        return {"message": "Guardian not found"}, 404
