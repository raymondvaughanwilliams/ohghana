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


class NotesForm(FlaskForm):
    text = TextAreaField('Text')
    submit = SubmitField('Add Note')



class UpdateSessionForm(FlaskForm):
    date = DateField('Choose Date', [validators.DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time',[validators.DataRequired()])
    submit = SubmitField('Reschedule')


class SessionForm(FlaskForm):
    session  = SelectField('Route',validators=[DataRequired()],choices=[(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)])
    submit = SubmitField('Update sessions')


class JournalForm(FlaskForm):
    date = DateField('Choose Date', [validators.DataRequired()],format='%d-%m-%Y')
    text = StringField('Text', [validators.DataRequired()])
    title = StringField('Title')
    submit = SubmitField('Add')


class Addtherapist(Form):
    title = StringField('Title', [validators.DataRequired()])
    
    
class AppointmentForm(Form):
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])
    # user_confirmation  = SelectField('User c',validators=[DataRequired()],choices=[('1', '1'), ('2', '2'),('3', '3'), ('4', '4'), ('5','5'), ('6', '6'), ('7', '7'), ('8','8'), ('9', '9'), ('10', '10')])
    # therapist_confirmation = SelectField('Route',validators=[DataRequired()],choices=[('1', '1'), ('2')])
    platform = StringField('Platform',validators=[DataRequired()])
    user_notes = StringField('User Notes')
    therapist_notes = StringField('Therapist Notes')
    submit = SubmitField('Submit')
    
    
class ContactForm(Form):
    name = StringField('Name')
    email = StringField('Email', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    hidden = HiddenField('Hidden',default="contact" )
    hidden_feedback = HiddenField('Hidden',default="feedback" )

    submit = SubmitField('Submit')
    
    

class FeedbackForm(Form):
    name = StringField('Name')
    email = StringField('Email', validators=[DataRequired()])
    text = StringField('Text', validators=[DataRequired()])
    hidden = HiddenField('Hidden',default="contact" )
    submit = SubmitField('Submit')
    
    
    
class NewThreadForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Post', validators=[DataRequired()])
    anonymous = BooleanField('Anonymous', default=False)
    submit = SubmitField('Submit')