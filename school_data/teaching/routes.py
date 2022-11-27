from flask import Blueprint, render_template, redirect, flash
from school_data.teaching.forms import AddTeachingForm
from school_data import db
from school_data.models import Student, Group, Subject, Teacher, Teaching

teachingS = Blueprint('teachingS', __name__)


@teachingS.route('/add_teaching', methods=["POST", "GET"])
def add_teaching():
    def group_query():
        return Group.query

    def subject_query():
        return Subject.query

    def teacher_query():
        return Teacher.query

    form = AddTeachingForm()
    form.group.query_factory = group_query
    form.subject.query_factory = subject_query
    form.teacher.query_factory = teacher_query

    if form.validate_on_submit():
        current_teaching = \
            Teaching(
                group=form.group.data,
                subject=form.subject.data,
                teacher=form.teacher.data
            )

        db.session.add(current_teaching)
        db.session.commit()
        flash('Operation is successful', 'success')

        return render_template('addTeachingForm.html',
                               form=form,
                               title='Add teaching')

    return render_template('addTeachingForm.html',
                           form=form,
                           title='Add teaching')
