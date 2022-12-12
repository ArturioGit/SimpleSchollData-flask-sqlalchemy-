from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField


class AddTeachingForm(FlaskForm):
    group = QuerySelectField('Class', query_factory=[], allow_blank=True, validators=[DataRequired()])
    subject = QuerySelectField('Subject', query_factory=[], allow_blank=True, validators=[DataRequired()])
    teacher = QuerySelectField('Teacher', query_factory=[], allow_blank=True, validators=[DataRequired()])
    submit = SubmitField('Add')


class EditTeachingForm(AddTeachingForm):
    submit = SubmitField('Edit')