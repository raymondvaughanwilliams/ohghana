from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class FaqForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    question = StringField('Question', validators=[DataRequired()])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('SUBMIT')