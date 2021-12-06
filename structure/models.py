#models.py
from structure import db,login_manager,app
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    password_hash = db.Column(db.String(128))

    posts = db.relationship('WebFeature',backref='author',lazy=True)

    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"


class WebFeature(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    text = db.Column(db.Text,nullable=False)


    def __init__(self,title,text,user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}---{self.text}"




class About(db.Model):


    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(140),nullable=False)
    subtitle= db.Column(db.String(140),nullable=True)
    text = db.Column(db.Text,nullable=False)
    image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    location = db.Column(db.String(140),nullable=False,default='location')
    number = db.Column(db.Integer,nullable=True)
    email = db.Column(db.String(64),unique=True,index=True)
    contact_subtitle = db.Column(db.String(140),nullable=True)
    about_subtitle = db.Column(db.String(140),nullable=True)
    feature_subtitle = db.Column(db.String(140),nullable=True)
    feature_paragraph = db.Column(db.Text,nullable=True)
    faq_title = db.Column(db.String(140),nullable=True)
    faq_subtitle = db.Column(db.String(140),nullable=True)
    faq_paragraph = db.Column(db.String(140),nullable=True)
    testimonial_title = db.Column(db.String(140),nullable=True)
    testimonial_subtitle = db.Column(db.String(140),nullable=True)
    testimonial_paragraph = db.Column(db.String(140),nullable=True)
    team_title = db.Column(db.String(140),nullable=True)
    team_subtitle = db.Column(db.String(140),nullable=True)
    team_paragraph = db.Column(db.String(140),nullable=True)

    def __init__(self,title,text,user_id,location,number,email,contact_subtitle,about_subtitle,
    feature_subtitle,feature_paragraph,faq_title,faq_subtitle,faq_paragraph,testimonial_title,
    testimonial_subtitle,testimonial_paragraph,team_title,team_subtitle,team_paragraph):
        self.title = title
        self.text = text
        self.location = location
        self.number = number
        self.email = email
        self.contact_subtitle = contact_subtitle
        self.about_subtitle = about_subtitle
        self.feature_subtitle = feature_subtitle
        self.feature_paragraph = feature_paragraph
        self.faq_title = faq_title
        self.faq_subtitle = faq_subtitle
        self.faq_paragraph = faq_paragraph
        self.testimonial_title = testimonial_title
        self.testimonial_subtitle = testimonial_subtitle
        self.testimonial_paragraph = testimonial_paragraph
        self.team_title = team_title
        self.team_subtitle = team_subtitle
        self.team_paragraph = team_paragraph

    def __repr__(self):
        return f"Post ID: {self.id} -- {self.title} -- {self.location} -- {self.number} -- {self.email} -- {self.contact_subtitle}-- {self.about_subtitle}-- {self.feature_subtitle}-- {self.feature_paragraph}-- {self.faq_title}-- {self.faq_subtitle}-- {self.faq_paragraph}-- {self.testimonial_title}-- {self.testimonial_subtitle}-- {self.testimonial_paragraph}-- {self.team_title}-- {self.team_subtitle}-- {self.team_paragraph}"



class Price(db.Model):


    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(140),nullable=False)
    amount = db.Column(db.Text,nullable=False)
    features = db.Column(db.Text(64),nullable=False,default='default_profile.png')

    def __init__(self,title,amount,features):
        self.title = title
        self.amount = amount
        self.features = features 

    def __repr__(self):
        return f"Post ID: {self.id} -- {self.title}"




class Faq(db.Model):


    id = db.Column(db.Integer,primary_key=True)
    question = db.Column(db.String(140),nullable=False)
    answer = db.Column(db.Text,nullable=False)

    def __init__(self,question,answer):
        self.question = question
        self.answer = answer

    def __repr__(self):
        return f"{self.question} -- {self.answer}"




class Testimonial(db.Model):


    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    company = db.Column(db.String,nullable=True)
    text = db.Column(db.String(140),nullable=True)
    rating = db.Column(db.Integer,nullable=True)


    def __init__(self,name,company,text,rating):
        self.name = name
        self.company = company
        self.text = text
        self.rating = rating

    def __repr__(self):
        return f"Post ID: {self.id} -- {self.name} -- {self.company} -- {self.text} -- {self.rating}"




class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=True)
    position = db.Column(db.String,nullable=True)
    faceboook = db.Column(db.String(140),nullable=True)
    instagram = db.Column(db.Integer,nullable=True)
    twitter = db.Column(db.Integer,nullable=True)


    def __init__(self,name,position,faceboook,instagram,twitter):
        self.name = name
        self.position = position
        self.faceboook = faceboook
        self.instagram = instagram
        self.twitter = twitter

    def __repr__(self):
        return f"{self.name} -- {self.position} -- {self.faceboook} -- {self.instagram} -- {self.twitter}"