from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from school_data.models import Group
import re


class AddGroupForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        # Checking the correctness of the class name
        template = r"1(0|1)-[A-Z]"
        second_template = r'\b[1-9]-[A-Z]\b'

        is_correct = re.findall(template, name.data)
        second_is_correct = re.findall(second_template, name.data)

        if not (is_correct or second_is_correct):
            raise ValidationError('Name should be like: 1-B, 11-A, 7-B ...')

        # Checking the presence of the name in the table
        if Group.query.filter_by(name=name.data).first():
            raise ValidationError('This class already exists')
