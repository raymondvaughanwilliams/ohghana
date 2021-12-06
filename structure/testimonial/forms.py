from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired


class TestimonialForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    name = StringField('Name', validators=[DataRequired()])
    company = StringField('Company', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired()])
    submit = SubmitField('SUBMIT')