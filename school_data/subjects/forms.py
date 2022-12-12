from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from school_data.models import Subject
import re


class AddSubjectForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=25)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        # Checking the correctness of the subject name
        template = r"\b[A-Z][\w_]+$"

        is_correct = re.findall(template, name.data)

        if not is_correct:
            raise ValidationError('Name should be like: Biology_and_ecology, Chemistry')

        # Checking the presence of the name in the table
        if Subject.query.filter_by(name=name.data).first():
            raise ValidationError('This subject already exists')


class EditSubjectForm(AddSubjectForm):
    submit = SubmitField('Edit')