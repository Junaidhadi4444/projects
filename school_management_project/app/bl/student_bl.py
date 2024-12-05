# app/bl/student_bl.py
from app.repo.student_repo import StudentRepository
from app.models.student import Student
from app.schemas.student_schema import StudentSchema
from marshmallow import ValidationError
from app.repo.parent_repo import ParentRepository

class StudentBL:
    @staticmethod
    def get_all_students():
        students = StudentRepository.get_all_students()
        return students
    
    @staticmethod
    def get_student_by_id(student_id):
        student = StudentRepository.get_student_by_id(student_id)
        if student:
            student_schema = StudentSchema()
            return student_schema.dump(student), 200  # Serialize student data
        return {"message": "Student not found"}, 404
    
    @staticmethod
    def create_student(data):
        try:
            # Validate and deserialize data
            student_schema = StudentSchema()
            student_data = student_schema.load(data)

            # Create a new student
            student = StudentRepository.create_student(student_data)
            return student, 201
        except ValidationError as e:
            return {"error": str(e)}, 400

    @staticmethod
    def update_student(student_id, data):
        student = StudentRepository.get_student_by_id(student_id)
        if student:
            try:
                # Validate and deserialize data
                student_schema = StudentSchema()
                updated_data = student_schema.load(data, partial=True)
                student = StudentRepository.update_student(student_id, updated_data)
                return student, 200
            except ValidationError as e:
                return {"error": str(e)}, 400
        return {"message": "Student not found"}, 404

    @staticmethod
    def delete_student(student_id):
        student = StudentRepository.get_student_by_id(student_id)
        if student:
            StudentRepository.delete_student(student_id)
            return {"message": "Student deleted successfully"}, 200
        return {"message": "Student not found"}, 404
    
    @staticmethod
    def associate_parent(student_id, parent_id):
        """Associate a parent with a student."""
        student = StudentRepository.get_student_by_id(student_id)
        parent = ParentRepository.get_parent(parent_id)
        if student and parent:
            student.parents.append(parent)
            StudentRepository.save(student)
            return {"message": "Parent associated with student successfully"}, 200
        return {"message": "Student or Parent not found"}, 404

    @staticmethod
    def dissociate_parent(student_id, parent_id):
        """Dissociate a parent from a student."""
        student = StudentRepository.get_student_by_id(student_id)
        parent = ParentRepository.get_parent(parent_id)
        if student and parent:
            if parent in student.parents:
                student.parents.remove(parent)
                StudentRepository.save(student)
                return {"message": "Parent dissociated from student successfully"}, 200
            return {"message": "Parent not associated with student"}, 400
        return {"message": "Student or Parent not found"}, 404
