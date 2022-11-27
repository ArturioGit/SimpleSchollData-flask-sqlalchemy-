from flask import Blueprint, render_template, redirect, flash
from school_data.classes.forms import AddGroupForm
from school_data import db
from school_data.models import Group

groups = Blueprint('groups', __name__)


@groups.route('/add_group', methods=["POST", "GET"])
def add_group():
    form = AddGroupForm()

    if form.validate_on_submit():
        group_name = form.name.data

        current_group = \
            Group(
                name=group_name
            )

        db.session.add(current_group)
        db.session.commit()
        flash('Operation is successful', 'success')

        return render_template('addGroupForm.html',
                               form=form,
                               title='Add class')

    return render_template('addGroupForm.html',
                           form=form,
                           title='Add class')
