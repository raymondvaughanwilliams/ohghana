from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField
from wtforms.validators import DataRequired


class BlockForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    name = StringField('NName', validators=[DataRequired()])
    # select field with active and inactive options
    status = SelectField('Status', choices=[('active', 'Active'), ('inactive', 'Inactive')])
    submit = SubmitField('SUBMIT')