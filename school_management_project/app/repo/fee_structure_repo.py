from app.db import db
from app.models.fee_structure import FeeStructure

class FeeStructureRepository:
    @staticmethod
    def get_all_fee_structures():
        return FeeStructure.query.all() 
    
    @staticmethod
    def get_fee_structure(id):
        return FeeStructure.query.get(id)
    
    @staticmethod
    def create_fee_structure(fee_structure):
        db.session.add(fee_structure)
        db.session.commit()
        return fee_structure    

    @staticmethod
    def update_fee_structure(fee_structure):
        db.session.commit() 

    @staticmethod
    def delete_fee_structure(fee_structure):
        db.session.delete(fee_structure)
        db.session.commit()
        return True
