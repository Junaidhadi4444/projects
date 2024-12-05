from app.repo.parent_repo import ParentRepository
from app.models.parent import Parent
from app.schemas.parent_schema import ParentSchema
from marshmallow import ValidationError

class ParentBL:
    @staticmethod
    def get_all_parents():
        parents = ParentRepository.get_all_parents()
        parent_schema = ParentSchema()
        return parent_schema.dump(parents, many=True)
    
    @staticmethod
    def get_parent_by_id(parent_id):
        parent = ParentRepository.get_parent(parent_id)
        if parent:
            parent_schema = ParentSchema()
            return parent_schema.dump(parent), 200
        return {"message": "Parent not found"}, 404
    
    @staticmethod
    def create_parent(data):
        try:
            # Validate and deserialize data
            parent_schema = ParentSchema()
            parent_data = parent_schema.load(data)

            # Create a new parent
            parent = Parent(**parent_data)
            ParentRepository.create_parent(parent_data)
            return parent_schema.dump(parent), 201
        except ValidationError as e:
            return {"error": str(e)}, 400

    @staticmethod
    def update_parent(parent_id, data):
        """
        Update a parent using their ID and the provided data.
        """
        # Retrieve the parent object from the repository
        parent = ParentRepository.get_parent(parent_id)
        if not parent:
            return {"message": "Parent not found"}, 404
        
        try:
            # Validate and deserialize the input data
            parent_schema = ParentSchema()
            updated_data = parent_schema.load(data, partial=True)
            
            # Update the parent object with the deserialized data
            for key, value in updated_data.items():
                setattr(parent, key, value)
            
            # Save the updated parent object to the repository
            ParentRepository.update_parent(parent_id, updated_data)
            
            return parent_schema.dump(parent), 200
        
        except ValidationError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500


    @staticmethod
    def delete_parent(parent_id):
        parent = ParentRepository.get_parent(parent_id)
        if parent:
            ParentRepository.delete_parent(parent_id)
            return {"message": "Parent deleted"}, 200
        return {"message": "Parent not found"}, 404
    

    @staticmethod
    def get_students_of_parent(parent_id):
        """Retrieve all students associated with a parent."""
        parent = ParentRepository.get_parent(parent_id)
        if parent:
            students = parent.students
            return {"students": [student.full_name for student in students]}, 200
        return {"message": "Parent not found"}, 404