from app.db import db
from app.models.teacher import Teacher

class TeacherRepository:
    @staticmethod
    def create(data):
        new_teacher = Teacher(
            first_name=data['first_name'],
            last_name=data['last_name'],
            full_name=data['full_name'],
            father_name=data['father_name'],
            status=data['status'],
            subject=data['subject'],
            qualification=data['qualification'],
            email=data['email']
        )
        db.session.add(new_teacher)
        db.session.commit()
        return new_teacher 

    @staticmethod
    def get_by_id(teacher_id):
        teacher = Teacher.query.get(teacher_id)
        return teacher
    
    @staticmethod
    def update(teacher):
        db.session.commit() 

    @staticmethod
    def get_all():
        return Teacher.query.all()
    
    @staticmethod
    def get_classes_by_teacher(teacher_id):
        teacher = Teacher.query.get(teacher_id)
        if teacher:
            return teacher.classes  # Retrieve all classes taught by the teacher
        return []

    @staticmethod
    def update_teacher(id, data):
        teacher = Teacher.query.get(id)
        if teacher:
            teacher.first_name = data.get('first_name', teacher.first_name)
            teacher.last_name = data.get('last_name', teacher.last_name)
            teacher.full_name = data.get('full_name', teacher.full_name)
            teacher.father_name = data.get('father_name', teacher.father_name)
            teacher.status = data.get('status', teacher.status)
            teacher.subject = data.get('subject', teacher.subject)
            teacher.qualification = data.get('qualification', teacher.qualification)
            teacher.email = data.get('email', teacher.email)
            db.session.commit()
            return teacher
        return None

    @staticmethod
    def delete_teacher(id):
        teacher = Teacher.query.get(id)  # Check if the teacher exists
        if not teacher:
            return False  # Return False if the teacher is not found
        
        db.session.delete(teacher)
        db.session.commit()
        return True  # Return True only if deletion is successful
