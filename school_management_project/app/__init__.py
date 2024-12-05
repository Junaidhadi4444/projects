#app/__init__.py
from flask import Flask
from flask_marshmallow import Marshmallow
from blueprints.teachers import teacher_bp
from blueprints.students import student_bp
from blueprints.parents import parent_bp
from blueprints.guardians import guardian_bp
from blueprints.classes import class_bp
from blueprints.fee_structure import fee_structure_bp
from app.db import db

ma=Marshmallow()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/school_management_project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #app.config['SECRET_KEY'] = 'secret_key' 

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(teacher_bp, url_prefix='/teachers')
    app.register_blueprint(student_bp, url_prefix='/students')
    app.register_blueprint(parent_bp, url_prefix='/parents')
    app.register_blueprint(guardian_bp, url_prefix='/guardians')
    app.register_blueprint(class_bp, url_prefix='/classes')
    app.register_blueprint(fee_structure_bp, url_prefix='/fee_structure')
    # Create tables if not already present
    with app.app_context():
        db.create_all()

    return app