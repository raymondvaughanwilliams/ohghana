
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_wtf.file import FileField,FileAllowed








class UpdateTeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    position = StringField('Positioon', validators=[DataRequired()])
    facebook = StringField('Facebook', validators=[DataRequired()])
    twitter = StringField('Twitter', validators=[DataRequired()])
    instagram = StringField('Instagram', validators=[DataRequired()])
    link = StringField('Firebase Link')
    picture = FileField('Update Teammate Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add Teammate')



class TeamForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    position = StringField('Position', validators=[DataRequired()])
    facebook = StringField('Facebook', validators=[DataRequired()])
    twitter = StringField('Twitter', validators=[DataRequired()])
    instagram = StringField('Instagram', validators=[DataRequired()])
    link = StringField('Firebase Link')
    picture = FileField('Update Teammate Picture', validators=[FileAllowed(['jpg', 'png'])])
    link = StringField('Firebase Link')

    submit = SubmitField('Update')
