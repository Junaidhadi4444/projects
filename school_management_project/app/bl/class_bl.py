from app.repo.class_repo import ClassRepository
from app.models.classs import Class
from app.schemas.class_schema import ClassSchema
from app.repo.student_repo import StudentRepository
from marshmallow import ValidationError

class ClassBL:
    @staticmethod
    def get_all_classes():
        classes=ClassRepository.get_all_classes()
        return classes
    
    @staticmethod
    def get_class_by_id(class_id):
        new_class = ClassRepository.get_class(class_id)
        if new_class:
            class_schema = ClassSchema()
            return class_schema.dump(new_class), 200
        return {"message": "Class not found"}, 404
        
    
    @staticmethod
    def create_class(data):
        try:
            class_schema = ClassSchema()
            class_data = class_schema.load(data)

            if 'teacher_id' not in class_data:
                return {"error": "Teacher ID is required to associate a class with a teacher."}, 400

            new_class = ClassRepository.create_class(class_data) 
            # If students are provided, associate them with the class
            if 'students' in class_data:
                for student_data in class_data['students']:
                    student_data['class_id'] = new_class.id  # Assign class_id to students
                    StudentRepository.create_student(student_data) 

            return class_schema.dump(new_class), 201
        except ValidationError as e:
            return {"error": str(e)}, 400

    @staticmethod
    def update_class(class_id, data):
        new_class = ClassRepository.get_class(class_id)
        if new_class:
            try:
                class_schema = ClassSchema()
                updated_data = class_schema.load(data, partial=True)
                new_class.class_name = updated_data.get('class_name', new_class.class_name)
                new_class.section = updated_data.get('section', new_class.section)

                # Update teacher association if provided
                if 'teacher_id' in updated_data:
                    new_class.teacher_id = updated_data['teacher_id']
                ClassRepository.update_class(class_id, updated_data)

                # If students are provided, update their class_id
                if 'students' in updated_data:
                    for student_data in updated_data['students']:
                        student_data['class_id'] = class_id  # Assign class_id to students
                        StudentRepository.update_student(student_data['id'], student_data)
                        
                return class_schema.dump(new_class), 200
            except ValidationError as e:
                return {"error": str(e)}, 400
        return {"message": "Class not found"}, 404

    @staticmethod
    def delete_class(class_id):
        new_class = ClassRepository.get_class(class_id)
        if new_class:
            ClassRepository.delete_class(class_id)
            return {"message": "Class deleted"}, 200
        return {"message": "Class not found"}, 404