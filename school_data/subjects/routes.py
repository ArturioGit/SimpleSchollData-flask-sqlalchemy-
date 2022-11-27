from flask import Blueprint, render_template, redirect, flash
from school_data.subjects.forms import AddSubjectForm
from school_data import db
from school_data.models import Subject

subjects = Blueprint('subjects', __name__)


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
        flash('Operation is successful', 'success')

        return render_template('addSubjectForm.html',
                               form=form,
                               title='Add subject')

    return render_template('addSubjectForm.html',
                           form=form,
                           title='Add subject')
