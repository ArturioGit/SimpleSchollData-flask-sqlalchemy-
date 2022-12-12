from flask import Blueprint, render_template, redirect, flash, request
from school_data.subjects.forms import AddSubjectForm, EditSubjectForm
from school_data import db
from school_data.models import Subject
from school_data.utils import url_history_util

subjects = Blueprint('subjects', __name__)


@subjects.after_request
def save_response(response):
    return url_history_util.save_response(response)


@subjects.route('/add_subject', methods=["POST", "GET"])
def add_subject():
    form = AddSubjectForm()

    if form.validate_on_submit():
        subject_name = form.name.data

        current_subject = \
            Subject(
                name=subject_name
            )

        db.session.add(current_subject)
        db.session.commit()

        return redirect(url_history_util.url_back('main.about'))

    return render_template('addSubjectForm.html',
                           form=form,
                           title='Add subject')


@subjects.route('/show_subjects', methods=["POST", "GET"])
def show_subjects():
    page = request.args.get('page', 1, type=int)
    subjects_query = Subject.query.order_by(Subject.name.asc())
    subjects_paginate = db.paginate(subjects_query, page=page, per_page=8)
    return render_template('subjects.html', subjects_paginate=subjects_paginate, page=page)


@subjects.route('/edit_subject/<int:id>', methods=["POST", "GET"])
def edit_subject(id):
    subject = Subject.query.get_or_404(id)

    form = EditSubjectForm()

    if request.method != 'POST':
        form.name.default = subject.name
        form.process()

    if form.validate_on_submit():
        subject.name = form.name.data
        db.session.commit()

        return redirect(url_history_util.url_back('main.about'))

    return render_template('editSubjectForm.html',
                           form=form,
                           title='Edit subject',
                           id=subject.id)


@subjects.route('/delete_subject/<int:id>', methods=["GET"])
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    if subject.teachingS:
        flash("You cannot delete a subject taught to students", "error")
        return redirect(url_history_util.url_back('main.about'))
    db.session.delete(subject)
    db.session.commit()

    return redirect(url_history_util.url_back('main.about'))


