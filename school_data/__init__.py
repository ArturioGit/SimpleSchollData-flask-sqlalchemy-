from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    from school_data.main.routes import main
    from school_data.classes.routes import groups
    from school_data.subjects.routes import subjects
    from school_data.teachers.routes import teachers
    from school_data.students.routes import students
    from school_data.teaching.routes import teachingS
    db.init_app(app)
    app.register_blueprint(main)
    app.register_blueprint(groups)
    app.register_blueprint(subjects)
    app.register_blueprint(teachers)
    app.register_blueprint(students)
    app.register_blueprint(teachingS)
    return app


"""app = create_app()
    db = SQLAlchemy(app)"""

"""with app.app_context():
    from school_data.models import Group, Subject, Student, Teacher, Teaching
    
    db.session.add(artur_student)
    db.session.commit()"""
