from app.repo.teacher_repo import TeacherRepository
from app.models.teacher import Teacher
from app.schemas.teacher_schema import TeacherSchema
from app.schemas.class_schema import ClassSchema
from marshmallow import ValidationError

class TeacherBL:
    def __init__(self):
        self.teacher_repo = TeacherRepository()

    def get_all_teachers(self):
        return self.teacher_repo.get_all()
    
    @staticmethod
    def get_teacher_by_id(teacher_id):
        teacher = TeacherRepository.get_by_id(teacher_id)
        if teacher:
            teacher_schema = TeacherSchema()
            return teacher_schema.dump(teacher), 200
        return {"message": "Teacher not found"}, 404
    
    @staticmethod
    def create_teacher(data):
        try:
            teacher_schema = TeacherSchema()
            teacher_data = teacher_schema.load(data)
            teacher = TeacherRepository.create(teacher_data)
            return teacher_schema.dump(teacher), 201
        except ValidationError as e:
            return {"error": str(e)}, 400
    
    @staticmethod
    def get_classes_by_teacher(teacher_id):
        teacher = TeacherRepository.get_by_id(teacher_id)
        if teacher:
            classes = TeacherRepository.get_classes_by_teacher(teacher_id)
            class_schema = ClassSchema(many=True)
            return class_schema.dump(classes), 200
        return {"message": "Teacher not found"}, 404

    @staticmethod
    def update_teacher(teacher_id, data):
        teacher = TeacherRepository.get_by_id(teacher_id)
        if teacher:
            try:
                teacher_schema = TeacherSchema()
                updated_data = teacher_schema.load(data, partial=True)
                teacher.first_name = updated_data.get('first_name', teacher.first_name)
                teacher.last_name = updated_data.get('last_name', teacher.last_name)
                teacher.full_name = updated_data.get('full_name', teacher.full_name)
                teacher.father_name = updated_data.get('father_name', teacher.father_name)
                teacher.status = updated_data.get('status', teacher.status)
                teacher.subject = updated_data.get('subject', teacher.subject)
                teacher.qualification = updated_data.get('qualification', teacher.qualification)
                teacher.email = updated_data.get('email', teacher.email)
                TeacherRepository.update(teacher)
                return teacher_schema.dump(teacher), 200
            except ValidationError as e:
                return {"error": str(e)}, 400
        return {"message": "Teacher not found"}, 404

    @staticmethod
    def delete_teacher(teacher_id):
        # Check if the teacher exists and delete
        success = TeacherRepository.delete_teacher(teacher_id)
        return success

