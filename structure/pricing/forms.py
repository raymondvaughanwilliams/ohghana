from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PriceForm(FlaskForm):
    # no empty titles or text possible
    # we'll grab the date automatically from the Model later
    title = StringField('Pricing Name', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    features = StringField('Features', validators=[DataRequired()])
    submit = SubmitField('Submit')
