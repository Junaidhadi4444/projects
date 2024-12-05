from app.db import db

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    father_name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    classes = db.relationship('Class', backref='teacher', lazy=True)
    
    def __repr__(self):
        return f'<Teacher {self.full_name}>'