from flask import Blueprint, render_template, redirect, flash, url_for
from school_data.classes.forms import AddGroupForm, EditGroupForm
from school_data import db
from school_data.models import Group
from school_data.sort_utils.sort_groups import sort_groups
from school_data.utils import url_history_util

groups = Blueprint('groups', __name__)


@groups.after_request
def save_response(response):
    return url_history_util.save_response(response)


@groups.route('/show_groups', methods=["GET"])
def show_groups():
    groups_query = sort_groups(Group.query)
    return render_template('groups.html', groups=groups_query)


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

        return redirect(url_for('groups.show_groups'))

    return render_template('addGroupForm.html',
                           form=form,
                           title='Add class')


@groups.route('/show_group/<int:id>', methods=["GET"])
def show_group(id):
    group = Group.query.get_or_404(id)
    return render_template('groupInfo.html', group=group)


@groups.route('/edit_group/<int:id>', methods=["POST", "GET"])
def edit_group(id):
    form = EditGroupForm()
    group = Group.query.get_or_404(id)
    if form.validate_on_submit():
        group_name = form.name.data
        group.name = group_name
        db.session.commit()

        return redirect(url_for('groups.show_group', id=id))

    return render_template('editGroupForm.html',
                           form=form,
                           title='Edit class')


@groups.route('/delete_group/<int:id>', methods=["POST", "GET"])
def delete_group(id):
    group = Group.query.get_or_404(id)
    if group.students:
        flash('You cannot delete a class that has students', 'error')
        return redirect(url_for('groups.show_group', id=id))
    if group.teachingS:
        flash('You cannot delete a class that has teaching', 'error')
        return redirect(url_for('groups.show_group', id=id))
    db.session.delete(group)
    db.session.commit()
    return redirect(url_for('groups.show_groups'))
