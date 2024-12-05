# app/repo/student_repo.py
from app.db import db
from app.models.student import Student
from app.models.classs import Class
from app.models.parent import Parent
from app.models.student_parent import student_parent


class StudentRepository:
    @staticmethod
    def create_student(data):
        #class_id=data.get(class_id)
        class_id = data.get('class_id')

        if class_id:
            student_class=Class.query.get(class_id)
            if not student_class:
                raise ValueError(' class not found')
            
        student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            full_name=data['full_name'],
            father_name=data['father_name'],
            guardian_name=data.get('guardian_name', None),  # Optional field
            status=data['status'],
            class_id=data['class_id']
        )
        db.session.add(student)
        db.session.commit()
        return student

    @staticmethod
    def get_student_by_id(id):
        return Student.query.get(id)

    @staticmethod
    def get_all_students():
        return Student.query.all()

    @staticmethod
    def update_student(id, data):
        student = Student.query.get(id)
        '''
        if student:
            class_id=data.get['class_id']
            if class_id:
                student_class=Class.query.get(class_id)
                if not student_class:
                    raise ValueError("class not found")
                student.class_id=class_id'''

        if student:
            student.first_name = data.get('first_name', student.first_name)
            student.last_name = data.get('last_name', student.last_name)
            student.full_name = data.get('full_name', student.full_name)
            student.father_name = data.get('father_name', student.father_name)
            student.guardian_name = data.get('guardian_name', student.guardian_name)
            student.status = data.get('status', student.status)
            student.class_id=data.get('class_id', student.class_id)
            db.session.commit()
            return student
        return None

    @staticmethod
    def delete_student(id):
        student = Student.query.get(id)
        if student:
            db.session.delete(student)
            db.session.commit()
            return True
        return False
    

    @staticmethod
    def add_parent_to_student(student_id, parent_id):
        student = Student.query.get(student_id)
        parent = Parent.query.get(parent_id)
        if student and parent:
            student.parents.append(parent)
            db.session.commit()
            return True
        return False

    @staticmethod
    def remove_parent_from_student(student_id, parent_id):
        student = Student.query.get(student_id)
        parent = Parent.query.get(parent_id)
        if student and parent:
            student.parents.remove(parent)
            db.session.commit()
            return True
        return False