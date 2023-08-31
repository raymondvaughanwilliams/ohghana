#models.py
from unicodedata import name
from structure import db,login_manager,app,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,LoginManager
from datetime import datetime

# class UserTherapySession(db.Model):
#     __tablename__ = 'usertherapysessions'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     user = db.relationship("User", foreign_keys=user_id)
#     booking_id = db.Column(db.Integer, db.ForeignKey('bookings.id'))


class User(db.Model,UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    profile_image = db.Column(db.String(64),nullable=False,default='default_profile.png')
    email = db.Column(db.String(64),unique=True,index=True)
    username = db.Column(db.String(64),unique=True,index=True)
    name = db.Column(db.String(64),nullable=True)
    last_name = db.Column(db.String(64),nullable=True)
    password_hash = db.Column(db.String(128))
    number = db.Column(db.String(128))
    location = db.Column(db.String(128))
    role = db.Column(db.String,nullable=True)
    phone_number = db.Column(db.String)
    biography = db.Column(db.String)
    status=db.Column(db.String,default="unverified")
    index_number = db.Column(db.String)
    completed_year=db.Column(db.String)
    # rec_payment_id = db.Column(db.Integer,db.ForeignKey('payments.id'),nullable=True)
    # payments = db.relationship('Payment',backref='users',lazy=True)


    # roles = db.relationship('Roles', secondary='user_roles')


    def __init__(self,email,username,password,name,role,last_name,number):
        self.email = email
        self.username = username
        self.name = name
        self.password_hash = generate_password_hash(password)
        self.role = role
        # self.rem_chatweeks = rem_chatweeks
        # self.rem_sessions=rem_sessions
        # self.pref_medium = pref_medium
        # self.pref_help = pref_help
        # self.pref_therapistgender = pref_therapistgender
        self.last_name = last_name
        self.number = number

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"Username {self.username}"





class About(db.Model):


    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(140),nullable=False)
    subtitle= db.Column(db.String(140),nullable=True)
    atext = db.Column(db.Text,nullable=True)
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




class SipRequest(db.Model):
    __tablename__ = "siprequests"
    id = db.Column(db.Integer, primary_key=True)
    channels = db.Column(db.String(128), nullable=True)
    other = db.Column(db.String(512), nullable=True)
    codecs = db.Column(db.Integer, nullable=True)
    inbound = db.Column(db.String(128), nullable=True)
    outbound = db.Column(db.String(128), nullable=True)
    provider = db.Column(db.String(128), nullable=True)
    certificate = db.Column(db.String(128), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=[user_id])
    status = db.Column(db.String(16), nullable=False,default="unverified")
    email = db.Column(db.String(106), nullable=True)
    name = db.Column(db.String(106), nullable=True)
    customer_id = db.Column(db.String(106), nullable=True)
    ip = db.Column(db.String(106), nullable=True)
    
    


    def __repr__(self):
        return f'<Part {self.name}>'





class Extension(db.Model):
    __tablename__ = "extensions"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(106), nullable=True)
    password = db.Column(db.String(106), nullable=True)
    ip = db.Column(db.String(106), nullable=True)
    channels = db.Column(db.String(106), nullable=True)
    company_id = db.Column(db.String(106), nullable=True)
    siprequest_id = db.Column(db.Integer, db.ForeignKey('siprequests.id'))
    siprequest = db.relationship("SipRequest", foreign_keys=[siprequest_id])

    def __repr__(self):
        return f'<Extension {self.name}>'



class AirtimeTopUp(db.Model):
    __tablename__ = "airtimetopups"
    id = db.Column(db.Integer, primary_key=True)
    payername = db.Column(db.String(106), nullable=True)
    payermobile = db.Column(db.String(106), nullable=True)
    payeremail = db.Column(db.String(106), nullable=True)
    recipientmobile = db.Column(db.String(106), nullable=True)
    amount = db.Column(db.String(106), nullable=True)
    merchtxnref = db.Column(db.String(106), nullable=True)
    countryid =db.Column(db.String(106), nullable=True)
    oprid =db.Column(db.String(106), nullable=True)
    vouchernumber =db.Column(db.String(106), nullable=True)
    type =db.Column(db.String(106), nullable=True)
    payerbankacctno =db.Column(db.String(106), nullable=True)
    payerbankaccttitle =db.Column(db.String(106), nullable=True)
    bankbranchsortcode =db.Column(db.String(106), nullable=True)
    payermsisdn =db.Column(db.String(106), nullable=True)
    recepientmsisdn =db.Column(db.String(106), nullable=True)
    
    

    def __repr__(self):
        return f'<Extension {self.name}>'




class CDR(db.Model):
    __tablename__ = "cdrs"
    id = db.Column(db.Integer, primary_key=True)
    call_type = db.Column(db.String(50))
    number = db.Column(db.String(20))
    call_direction = db.Column(db.String(50))
    name = db.Column(db.String(100))
    entity_id = db.Column(db.Integer)
    entity_type = db.Column(db.String(50))
    contact_id = db.Column(db.String(50))
    queue_extension = db.Column(db.String(20))
    agent = db.Column(db.String(50))
    agent_first_name = db.Column(db.String(50))
    agent_last_name = db.Column(db.String(50))
    agent_email = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    duration_timespan = db.Column(db.String(50))
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    call_start_time_local = db.Column(db.DateTime)
    call_start_time_utc = db.Column(db.DateTime)
    call_established_time_local = db.Column(db.DateTime)
    call_established_time_utc = db.Column(db.DateTime)
    call_end_time_local = db.Column(db.DateTime)
    call_end_time_utc = db.Column(db.DateTime)
    call_start_time_local_millis = db.Column(db.BigInteger)
    call_start_time_utc_millis = db.Column(db.BigInteger)
    call_established_time_local_millis = db.Column(db.BigInteger)
    call_established_time_utc_millis = db.Column(db.BigInteger)
    call_end_time_local_millis = db.Column(db.BigInteger)
    call_end_time_utc_millis = db.Column(db.BigInteger)
    subject = db.Column(db.String(200))
    inbound_call_text = db.Column(db.Text)
    missed_call_text = db.Column(db.Text)
    outbound_call_text = db.Column(db.Text)
    not_answered_outbound_call_text = db.Column(db.Text)  

    def __repr__(self):
        return f'<Extension {self.name}>' 
 

class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone_mobile = db.Column(db.String(20))
    phone_mobile2 = db.Column(db.String(20))
    phone_home = db.Column(db.String(20))
    phone_home2 = db.Column(db.String(20))
    phone_business = db.Column(db.String(20))
    phone_business2 = db.Column(db.String(20))
    phone_other = db.Column(db.String(20))
    contact_url = db.Column(db.String(200))
    entity_id = db.Column(db.Integer)
    entity_type = db.Column(db.String(50))

    def __repr__(self):
        return f'<Contact {self.phone_mobile}>'
    
    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
