from flask import Blueprint, render_template, redirect, flash, request, url_for, make_response
from school_data.teaching.forms import AddTeachingForm, EditTeachingForm
from school_data import db
from school_data.models import Student, Group, Subject, Teacher, Teaching
from school_data.sort_utils.sort_groups import sort_groups
from school_data.utils import url_history_util

teachingS = Blueprint('teachingS', __name__)


@teachingS.after_request
def save_response(response):
    return url_history_util.save_response(response)


@teachingS.route('/add_teaching', methods=["POST", "GET"])
def add_teaching():
    default_group_id = request.args.get("default_group_id", None, type=int)
    default_teacher_id = request.args.get("default_teacher_id", None, type=int)

    default_group = None if not default_group_id else Group.query.get_or_404(default_group_id)
    default_teacher = None if not default_teacher_id else Teacher.query.get_or_404(default_teacher_id)

    def group_query():
        return sort_groups(Group.query)

    def subject_query():
        return Subject.query

    def teacher_query():
        return Teacher.query

    form = AddTeachingForm()
    form.group.query_factory = group_query
    form.subject.query_factory = subject_query
    form.teacher.query_factory = teacher_query
    if request.method != 'POST':
        if default_group:
            form.group.default = default_group
        if default_teacher:
            form.teacher.default = default_teacher
        form.process()

    if form.validate_on_submit():
        current_teaching = \
            Teaching(
                group=form.group.data,
                subject=form.subject.data,
                teacher=form.teacher.data
            )

        db.session.add(current_teaching)
        db.session.commit()
        return redirect(url_history_util.url_back('main.about'))

    return render_template('addTeachingForm.html',
                           form=form,
                           title='Add teaching')


@teachingS.route('/show_teachingS/teacher/<int:id>', methods=["GET"])
def show_by_teacher(id):
    page = request.args.get("page", 1, type=int)
    teacher = Teacher.query.get_or_404(id)

    current_teachingS = Teaching.query.filter_by(teacher=teacher).order_by(Teaching.group_id)

    paginate_teachingS = db.paginate(current_teachingS, page=page, per_page=10)

    return render_template('GroupAndSubjectByTeacher.html', paginate_teachingS=paginate_teachingS, page=page,
                           teacher=teacher)


@teachingS.route('/show_teachingS/group/<int:id>', methods=["GET"])
def show_by_group(id):
    page = request.args.get("page", 1, type=int)
    group = Group.query.get_or_404(id)

    current_teachingS = Teaching.query.filter_by(group=group).order_by(Teaching.teacher_id)

    paginate_teachingS = db.paginate(current_teachingS, page=page, per_page=10)

    return render_template('TeacherAndSubjectByGroup.html', paginate_teachingS=paginate_teachingS, page=page,
                           group=group)


@teachingS.route('/edit_teaching/<int:id>', methods=["POST", "GET"])
def edit_teaching(id):
    teaching = Teaching.query.get_or_404(id)

    default_group_id = request.args.get("default_group_id", None, type=int)
    default_teacher_id = request.args.get("default_teacher_id", None, type=int)

    default_group = None if not default_group_id else Group.query.get_or_404(default_group_id)
    default_teacher = None if not default_teacher_id else Teacher.query.get_or_404(default_teacher_id)

    def group_query():
        return sort_groups(Group.query)

    def subject_query():
        return Subject.query

    def teacher_query():
        return Teacher.query

    form = EditTeachingForm()
    form.group.query_factory = group_query
    form.subject.query_factory = subject_query
    form.teacher.query_factory = teacher_query

    if request.method != 'POST':
        if default_group:
            form.group.default = default_group
        if default_teacher:
            form.teacher.default = default_teacher
        form.process()

    if form.validate_on_submit():
        teaching.teacher = form.teacher.data
        teaching.group = form.group.data
        teaching.subject = form.subject.data

        db.session.commit()

        return redirect(url_history_util.url_back('main.about'))
    return render_template('editTeachingForm.html',
                           form=form,
                           title='Edit teaching')


@teachingS.route('/delete_teaching/<int:id>', methods=["POST", "GET"])
def delete_teaching(id):
    teaching = Teaching.query.get_or_404(id)
    db.session.delete(teaching)
    db.session.commit()
    return redirect(url_history_util.url_back('main.about'))


