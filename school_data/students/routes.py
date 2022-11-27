from flask import Blueprint, render_template, redirect, flash
from school_data.students.forms import AddStudentForm
from school_data import db
from school_data.models import Student, Group

students = Blueprint('students', __name__)


@students.route('/add_student', methods=["POST", "GET"])
def add_student():

    def group_query():
        return Group.query

    form = AddStudentForm()
    form.group_id.query_factory = group_query

    if form.validate_on_submit():
        student_name = form.name.data
        student_surname = form.surname.data
        student_group = form.group_id.data
        current_student = \
            Student(
                name=student_name,
                surname=student_surname,
                group_id=student_group.id
            )

        db.session.add(current_student)
        db.session.commit()
        flash('Operation is successful', 'success')

        return render_template('addStudentForm.html',
                               form=form,
                               title='Add student')

    return render_template('addStudentForm.html',
                           form=form,
                           title='Add student')
