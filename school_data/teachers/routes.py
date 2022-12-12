from flask import Blueprint, render_template, redirect, flash, request, url_for
from school_data.teachers.forms import AddTeacherForm, EditTeacherForm
from school_data import db
from school_data.models import Teacher
from school_data.utils import url_history_util

teachers = Blueprint('teachers', __name__)


@teachers.after_request
def save_response(response):
    return url_history_util.save_response(response)


@teachers.route('/show_teachers', methods=["GET"])
def show_teachers():
    page = request.args.get("page", 1, type=int)

    teachers_group = db.paginate(
        db.select(Teacher).order_by(Teacher.surname.asc()), page=page, per_page=10
    )

    return render_template('teachers.html', teachers_group=teachers_group, page=page)


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


@teachers.route('/delete_teacher/<int:id>', methods=["POST", "GET"])
def delete_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    if teacher.teachingS:
        flash('You cannot delete a teacher that has teaching', 'error')
        return redirect(url_for('teachers.show_teachers'))
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('teachers.show_teachers'))


@teachers.route('/edit_teacher/<int:id>', methods=["POST", "GET"])
def edit_teacher(id):
    teacher = Teacher.query.get_or_404(id)
    form = EditTeacherForm()

    if request.method != 'POST':
        form.name.default = teacher.name
        form.surname.default = teacher.surname
        form.process()

    if form.validate_on_submit():
        teacher.name = form.name.data
        teacher.surname = form.surname.data
        db.session.commit()
        return redirect(url_for('teachers.show_teachers'))

    return render_template('editTeacherForm.html', form=form,
                           title='Edit teacher')
