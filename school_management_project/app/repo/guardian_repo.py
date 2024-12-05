from app.db import db
from app.models.guardian import Guardian

class GuardianRepository:
    @staticmethod
    def get_all_guardians():
        return Guardian.query.all()
    
    @staticmethod
    def get_guardian(id):
        return Guardian.query.get(id)
    
    @staticmethod
    def create_guardian(data):  
        guardian = Guardian(
            first_name=data['first_name'],
            last_name=data['last_name'],
            full_name=data['full_name'],
            father_name=data['father_name'],
            husband_name=data['husband_name'],
            phone_number=data['phone_number']
        )
        db.session.add(guardian)
        db.session.commit()
        return guardian
    
    @staticmethod
    def update_guardian(guardian):
        db.session.commit()

    @staticmethod
    def delete_guardian(guardian):
        db.session.delete(guardian)
        db.session.commit()
        return True
