from flask import Blueprint, render_template, redirect, flash
from school_data.teachers.forms import AddTeacherForm
from school_data import db
from school_data.models import Teacher

teachers = Blueprint('teachers', __name__)


@teachers.route('/add_teacher', methods=["POST", "GET"])
def add_teacher():
    form = AddTeacherForm()

    if form.validate_on_submit():
        teacher_name = form.name.data
        teacher_surname = form.surname.data
        current_teacher = \
            Teacher(
                name=teacher_name,
                surname=teacher_surname
            )

        db.session.add(current_teacher)
        db.session.commit()
        flash('Operation is successful', 'success')

        return render_template('addTeacherForm.html',
                               form=form,
                               title='Add teacher')

    return render_template('addTeacherForm.html',
                           form=form,
                           title='Add teacher')
