from flask import Blueprint, render_template, redirect, flash, request, url_for
from school_data.students.forms import AddStudentForm, EditStudentForm
from school_data import db
from school_data.models import Student, Group
from school_data.utils import url_history_util

students = Blueprint('students', __name__)


@students.after_request
def save_response(response):
    return url_history_util.save_response(response)


@students.route('/show_students/<int:group_id>', methods=["GET", "POST"])
def show_students(group_id):
    page = request.args.get("page", 1, type=int)
    current_group = Group.query.get_or_404(group_id)

    students_group = db.paginate(
        db.select(Student).filter_by(group_id=group_id).order_by(Student.surname.asc()), page=page, per_page=10
    )

    return render_template('students.html', students_group=students_group, current_group=current_group, page=page)


@students.route('/add_student', methods=["POST", "GET"])
def add_student():
    group_id = request.args.get('group_id', 1, type=int)

    current_group = Group.query.get_or_404(group_id)

    def group_query():
        return Group.query

    form = AddStudentForm()
    form.group_id.query_factory = group_query
    if request.method != 'POST':
        form.group_id.default = current_group
        form.process()

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

        return redirect(url_history_util.url_back(fallback='main.about'))

    return render_template('addStudentForm.html',
                           form=form,
                           title='Add student')


@students.route('/delete_student/<int:id>', methods=["POST", "GET"])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_history_util.url_back(fallback='main.about'))


@students.route('/edit_student/<int:id>', methods=["POST", "GET"])
def edit_student(id):
    def group_query():
        return Group.query

    student = Student.query.get_or_404(id)
    group_id = student.group_id

    group = Group.query.get_or_404(group_id)

    form = EditStudentForm()
    form.group_id.query_factory = group_query

    if request.method != 'POST':
        form.name.default = student.name
        form.surname.default = student.surname
        form.group_id.default = group
        form.process()

    if form.validate_on_submit():
        student.name = form.name.data
        student.surname = form.surname.data
        student.group_id = form.group_id.data.id
        db.session.commit()
        return redirect(url_history_util.url_back(fallback='main.about'))

    return render_template('editStudentForm.html', form=form,
                           title='Edit student')
