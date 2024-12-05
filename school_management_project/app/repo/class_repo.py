from app.db import db
from app.models.classs import Class

class ClassRepository:
    @staticmethod
    def get_all_classes():
        return Class.query.all()
    
    @staticmethod
    def get_class(id):
        return Class.query.get(id)

    @staticmethod
    def create_class(data):
        new_class = Class(
            class_name=data['class_name'],
            section=data['section'],
            teacher_id=data['teacher_id']  # Associate class with a teacher
        )
        db.session.add(new_class)
        db.session.commit()
        return new_class
    
    @staticmethod
    def get_students_for_class(class_id):
        # Retrieve all students associated with a particular class
        class_instance = Class.query.get(class_id)
        if class_instance:
            return class_instance.students  # Assuming `students` is the relationship field
        return None

    @staticmethod
    def update_class(id, data):
        new_class = Class.query.get(id)
        if new_class:
            new_class.class_name = data.get('class_name', new_class.class_name)
            new_class.section = data.get('section', new_class.section)
            new_class.teacher_id = data.get('teacher_id', new_class.teacher_id)
            db.session.commit()
            return new_class
        return None

    @staticmethod
    def delete_class(id):
        new_class = Class.query.get(id)
        if new_class:
            db.session.delete(new_class)
            db.session.commit()
            return True
        return False
    