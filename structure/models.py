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


    def __init__(self,email,username,password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"


class WebFeature(db.Model):


    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    wtext = db.Column(db.Text,nullable=False)


    def __init__(self,title,wtext):
        self.title = title
        self.wtext = wtext

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}---{self.text}"




class About(db.Model):


    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(140),nullable=False)
    subtitle= db.Column(db.String(140),nullable=True)
    atext = db.Column(db.Text,nullable=False)
    image = db.Column(db.String(64),nullable=True,default='default_profile.png')
    about_image = db.Column(db.String(64),nullable=True,default='default_profile.png')
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
    logo = db.Column(db.String(64),nullable=True,default='default_profile.png')
    carousel_image_1 = db.Column(db.String(64),nullable=True,default='default_profile.png')

    def __init__(self,title,text,user_id,location,number,email,contact_subtitle,about_subtitle,
    feature_subtitle,feature_paragraph,faq_title,faq_subtitle,faq_paragraph,testimonial_title,
    testimonial_subtitle,testimonial_paragraph,team_title,team_subtitle,team_paragraph,logo,carousel_image_1,subtitle,about_image):
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
        self.logo = logo
        self.subtitle = subtitle
        self.about_image = about_image
        self.carousel_image_1 = carousel_image_1

    def __repr__(self):
        return f"Post ID: {self.id} -- {self.title} -- {self.location} -- {self.number} -- {self.email} -- {self.contact_subtitle}-- {self.about_subtitle}-- {self.feature_subtitle}-- {self.feature_paragraph}-- {self.faq_title}-- {self.faq_subtitle}-- {self.faq_paragraph}-- {self.testimonial_title}-- {self.testimonial_subtitle}-- {self.testimonial_paragraph}-- {self.team_title}-- {self.team_subtitle}-- {self.team_paragraph} -- {self.logo} -- {self.carousel_image_1}"



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
    company = db.Column(db.String,nullable=True)
    name = db.Column(db.String,nullable=True)
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
    picture = db.Column(db.String(64),nullable=True)


    def __init__(self,name,position,faceboook,instagram,twitter,picture):
        self.name = name
        self.position = position
        self.faceboook = faceboook
        self.instagram = instagram
        self.twitter = twitter
        self.picture = picture

    def __repr__(self):
        return f"{self.name} -- {self.position} -- {self.faceboook} -- {self.instagram} -- {self.twitter}-- {self.picture}"








class Block(db.Model):
    __tablename__ = 'blocks'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=True)
    status = db.Column(db.String,nullable=True,default='active')
    block_type = db.Column(db.String,nullable=True,default='na')
    appearances= db.relationship('Appearance',backref='block',lazy=True)
    appearance_id = db.Column(db.Integer,db.ForeignKey('appearances.id'),nullable=True)


    def __init__(self,name,status,block_type):
        self.name = name
        self.status = status
        self.block_type = block_type

    def __repr__(self):
        return f"{self.name} -- {self.status} -- {self.block_type}"




#create table appearance with relationship to blocks
class Appearance(db.Model):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer,primary_key=True)
    # block_id = db.Column(db.Integer,db.ForeignKey('blocks.id'),nullable=False)
    # block = db.relationship('Block',backref=db.backref('appearance',lazy=True))
    title_color = db.Column(db.String(64),nullable=True)
    subtitle_color = db.Column(db.String(64),nullable=True)
    paragraph_color = db.Column(db.String(64),nullable=True)
    title_font = db.Column(db.String(64),nullable=True)
    subtitle_font = db.Column(db.String(64),nullable=True)
    paragraph_font = db.Column(db.String(64),nullable=True)
    title_size = db.Column(db.Integer,nullable=True)
    subtitle_size = db.Column(db.Integer,nullable=True)
    paragraph_size = db.Column(db.Integer,nullable=True)
    bootstrap_class1 = db.Column(db.String(64),nullable=True)
    bootstrap_class2 = db.Column(db.String(64),nullable=True)
    bootstrap_class3 = db.Column(db.String(64),nullable=True)
    

    def __init__(self,id,block_id,block,title_color,subtitle_color,paragraph_color,title_font,subtitle_font,paragraph_font,title_size,subtitle_size,paragraph_size,bootstrap_class1,bootstrap_class2,bootstrap_class3):
        self.id = id
        self.block_id = block_id
        self.block = block
        self.title_color = title_color
        self.subtitle_color = subtitle_color
        self.paragraph_color = paragraph_color
        self.title_font = title_font
        self.subtitle_font = subtitle_font
        self.paragraph_font = paragraph_font
        self.title_size = title_size
        self.subtitle_size = subtitle_size
        self.paragraph_size = paragraph_size
        self.bootstrap_class1 = bootstrap_class1
        self.bootstrap_class2 = bootstrap_class2
        self.bootstrap_class3 = bootstrap_class3



    def __repr__(self):
        return f"{self.id} -- {self.block_id} -- {self.block} -- {self.title_color} -- {self.subtitle_color} -- {self.paragraph_color} -- {self.title_font} -- {self.subtitle_font} -- {self.paragraph_font} -- {self.title_size} -- {self.subtitle_size} -- {self.paragraph_size} -- {self.bootstrap_class1} -- {self.bootstrap_class2} -- {self.bootstrap_class3}"