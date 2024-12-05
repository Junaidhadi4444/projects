from app.db import db
from app.models.parent import Parent
from app.models.student_parent import student_parent
from app.models.student import Student

class ParentRepository:
    @staticmethod
    def create_parent(data):
        parent = Parent(
            first_name=data['first_name'],
            last_name=data['last_name'],
            full_name=data['full_name'],
            husband_name=data['husband_name'],
            role=data['role'],
            phone_number=data['phone_number']
        )
        db.session.add(parent)
        db.session.commit()
        return parent

    @staticmethod
    def get_parent(id):
        return Parent.query.get(id)

    @staticmethod
    def get_all_parents():
        return Parent.query.all()

    @staticmethod
    def update_parent(id, data):
        parent = Parent.query.get(id)
        if parent:
            parent.first_name = data.get('first_name', parent.first_name)
            parent.last_name = data.get('last_name', parent.last_name)
            parent.full_name = data.get('full_name', parent.full_name)
            parent.husband_name = data.get('husband_name', parent.husband_name)
            parent.role = data.get('role', parent.role)
            parent.phone_number = data.get('phone_number', parent.phone_number)
            db.session.commit()
            return parent
        return None

    @staticmethod
    def delete_parent(id):
        parent = Parent.query.get(id)
        if parent:
            db.session.delete(parent)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def add_student_to_parent(parent_id, student_id):
        parent = Parent.query.get(parent_id)
        student = Student.query.get(student_id)
        if parent and student:
            parent.students.append(student)
            db.session.commit()
            return True
        return False

    @staticmethod
    def remove_student_from_parent(parent_id, student_id):
        parent = Parent.query.get(parent_id)
        student = Student.query.get(student_id)
        if parent and student:
            parent.students.remove(student)
            db.session.commit()
            return True
        return False
