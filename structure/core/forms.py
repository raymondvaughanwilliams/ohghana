from wtforms import BooleanField, StringField, PasswordField, validators , ValidationError, HiddenField,FloatField,IntegerField,SubmitField,SelectField,SelectMultipleField,TextAreaField,FileField,Form,DateTimeField,TimeField
from flask_wtf import FlaskForm, Form
from wtforms.fields.html5 import DateField,DateTimeField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from wtforms_components import TimeField


class BookingForm(FlaskForm):
    name = StringField('Contact Name', validators=[DataRequired(),Email()])
    # company = StringField('Company Name', [validators.Length(min=4, max=25)])
    date = DateField('Choose Date', [validators.DataRequired()] ,format='%Y-%m-%d')
    phone = StringField('Mobile', [validators.Length(min=6, max=35)])
    email = StringField('Email Address', validators=[DataRequired(),Email()])
    message = TextAreaField('Message', [validators.Length(min=4, max=140)]) 
    location = StringField('Location',[validators.Length(min=4,max=140)])
    time= TimeField('Time', [validators.DataRequired()])
    submit = SubmitField('BOOK THERAPIST')


class UpdateSessionForm(FlaskForm):
    date = DateField('Choose Date', [validators.DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time',[validators.DataRequired()])
    submit = SubmitField('Reschedule')



class JournalForm(FlaskForm):
    date = DateField('Choose Date', [validators.DataRequired()],format='%d-%m-%Y')
    text = StringField('Text', [validators.DataRequired()])
    title = StringField('Title')
    submit = SubmitField('Add')


class Addtherapist(Form):
    title = StringField('Title', [validators.DataRequired()])
    
    
class NewsletterForm(Form):
    name = StringField('Name')
    phone = StringField('Phone')
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Join Newsletter')
    