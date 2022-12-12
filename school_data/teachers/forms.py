from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
import re


class AddTeacherForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField('Add')

    def validate_name(self, name):
        # Checking the correctness of the class name
        template = r"\b[A-Z][a-z]+$"

        is_correct = re.findall(template, name.data)

        if not is_correct:
            raise ValidationError('Name should be like: George, Mykola, Kate')

    def validate_surname(self, surname):
        # Checking the correctness of the class name
        template = r"\b[A-Z][a-z]+$"

        is_correct = re.findall(template, surname.data)

        if not is_correct:
            raise ValidationError('Surname should be like: Holod, Smit, Klyuchka')


class EditTeacherForm(AddTeacherForm):
    submit = SubmitField('Edit')
