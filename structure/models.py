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
    business_name = db.Column(db.String)
    certificate = db.Column(db.String)
    parts = db.Column(db.String(250))
    cars = db.Column(db.String(250))
    returnable  = db.Column(db.String(250),default="no")
    return_period = db.Column(db.String(250),default="none")
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




class WebFeature(db.Model):
    __tablename__ = "webfeatures"


    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    title = db.Column(db.String(140),nullable=False)
    wtext = db.Column(db.Text,nullable=False)
    price = db.Column(db.Float,nullable=True)
    type = db.Column(db.String(100),nullable=True)
    email = db.Column(db.String(40),nullable=True)
    city = db.Column(db.String(50),nullable=True)
    phone = db.Column(db.String(50),nullable=True)



    def __init__(self,title,wtext,date):
        self.title = title
        self.wtext = wtext
        self.date = date
     

    def __repr__(self):
        return f"Post ID: --- {self.title}---{self.wtext}--{self.date}"




# class Therapist(db.Model):
#     __tablename__ = 'therapists'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     specialty = db.Column(db.String)
#     location = db.Column(db.String)
#     email = db.Column(db.String)
#     phone_number = db.Column(db.String)
#     biography = db.Column(db.String)
#     qualifications = db.Column(db.String)
#     years_of_experience = db.Column(db.Integer)
#     license_number = db.Column(db.String)
#     insurance_provider = db.Column(db.String)



# class TherapistDetails(db.Model):
#     __tablename__ = 'therapistdetails'

#     id = db.Column(db.Integer, primary_key=True)
#     specialty = db.Column(db.String)
#     location = db.Column(db.String)
#     email = db.Column(db.String)
#     phone_number = db.Column(db.String)
#     biography = db.Column(db.String)
#     qualifications = db.Column(db.String)
#     years_of_experience = db.Column(db.Integer)
#     license_number = db.Column(db.String)
#     insurance_provider = db.Column(db.String)
#     platforms = db.Column(db.String)
#     user_id = db.Column(db.Integer,db.ForeignKey('user.id'),nullable=True)
#     user= db.relationship('User',backref='users',lazy=True)
    
    



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
    __tablename__ = "prices"


    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(140),nullable=False)
    amount = db.Column(db.Text,nullable=False)
    features = db.Column(db.Text(64),nullable=False,default='default_profile.png')
    numsessions = db.Column(db.Integer,nullable=True)
    numchatweeks = db.Column(db.Integer,nullable=True)

    def __init__(self,title,amount,features,numsessions,numchatweeks):
        self.title = title
        self.amount = amount
        self.features = features 
        self.numsessions = numsessions
        self.numchatweeks = numchatweeks

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
    bootstrap_class1 = db.Column(db.String(64),nullable=True,default = 'col-md-4')
    bootstrap_class2 = db.Column(db.String(64),nullable=True,default = 'col-md-8')
    bootstrap_class3 = db.Column(db.String(64),nullable=True,default = 'col-md-12')
    

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
        return f"{self.id} -- -- {self.block} -- {self.title_color} -- {self.subtitle_color} -- {self.paragraph_color} -- {self.title_font} -- {self.subtitle_font} -- {self.paragraph_font} -- {self.title_size} -- {self.subtitle_size} -- {self.paragraph_size} -- {self.bootstrap_class1} -- {self.bootstrap_class2} -- {self.bootstrap_class3}"


class Book(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String,nullable=True)
    email = db.Column(db.String,nullable=True)
    date = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    phone = db.Column(db.String,nullable=True)
    location = db.Column(db.String,nullable=True)
    therapist_id = db.Column(db.Integer,db.ForeignKey('webfeatures.id'),nullable=True)
    message = db.Column(db.String,nullable=True)
    webfeatures= db.relationship('WebFeature',backref='bookings',lazy=True)
    time =  db.Column(db.Time, nullable=False, default=datetime.utcnow)
    users = db.relationship('User',backref='bookings',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)

    def __init__(self,name,email,date,phone,location,therapist_id,time,user_id,message):
        # self.id = id
        self.name = name
        self.email = email
        self.date = date
        self.phone = phone
        self.location = location
        self.therapist_id = therapist_id
        # self.webfeatures = webfeatures
        self.time = time
        # self.users = users
        self.user_id = user_id
        self.message = message

    def __repr__(self):
        return f"{self.id}--{self.name}"


# class Roles(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(50), nullable=False, unique=True)  # for @roles_accepted()

#     def __repr__(self):
#         return self.name


# # Define the UserRoles association model
# class UserRole(db.Model):
#     __tablename__ = 'user_roles'
#     id = db.Column(db.Integer(), primary_key=True)
#     user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
#     role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# # user_manager = LoginManager(app, db, User)
# login_manager = LoginManager(app, db, User)


class Journal(db.Model):
    __tablename__ = 'journals'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,nullable=True)
    date = db.Column(db.Date,nullable=True,default=datetime.utcnow)
    text = db.Column(db.String)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    users = db.relationship('User',backref='journals',lazy=True)



class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer,primary_key=True)
    amount = db.Column(db.Integer,nullable=True)
    date = db.Column(db.Date,nullable=True,default=datetime.utcnow)
    tx_ref = db.Column(db.String)
    transaction_id = db.Column(db.String)
    plan_id = db.Column(db.Integer,db.ForeignKey('prices.id'),nullable=True)
    plans = db.relationship('Price',backref='payments',lazy=True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=True)
    users = db.relationship('User',backref='payments',lazy=True)
    status = db.Column(db.String,nullable=True,default="Failed")




class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    time =  db.Column(db.Time)
    platform = db.Column(db.String(50))
    therapist_confirmation = db.Column(db.String(10),nullable=True)
    user_confirmation = db.Column(db.String(10),nullable=True)
    user = db.relationship("User", foreign_keys=[user_id])
    therapist = db.relationship("User", foreign_keys=[therapist_id])
    user_notes= db.Column(db.String(250))
    therapist_notes= db.Column(db.String(250))
    meeting_link = db.Column(db.String(250))
    
    
class NewsletterContacts(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=True)
    phone=db.Column(db.String(20))
    email=db.Column(db.String(50))
    
    
class Newsletter(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    recepients = db.Column(db.String(255),nullable=True)
    message = db.Column(db.String(255),nullable=True)
    date = db.Column(db.Date,default=datetime.now())
    


class Thread(db.Model):
    __tablename__ = 'threads'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('threads', lazy=True))
    anonymous = db.Column(db.Boolean, default=False)
    date = db.Column(db.Date,default=datetime.now())

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('posts', lazy=True))
    thread_id = db.Column(db.Integer, db.ForeignKey('threads.id'), nullable=False)
    thread = db.relationship('Thread', backref=db.backref('posts', lazy=True))
    main = db.Column(db.String(5),nullable=True)
    date = db.Column(db.Date,default=datetime.now())



class Note(db.Model):
    __tablename__ = 'notes'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", foreign_keys=[user_id])
    therapist_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    therapist = db.relationship("User", foreign_keys=[therapist_id])
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'))
    appointment = db.relationship("Appointment", foreign_keys=[appointment_id])
    
    
    
    
    
class Delivery(db.Model):
    __tablename__ = 'deliveries'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    sender = db.relationship("User", foreign_keys=[sender_id])
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    destination = db.relationship("Destination", foreign_keys=[destination_id])
    traveler_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    traveler = db.relationship("User", foreign_keys=[traveler_id])
    agent_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    agent = db.relationship("User", foreign_keys=[agent_id])
    delivery_status = db.Column(db.String(120), default="pending")
    item_name = db.Column(db.String(120))
    item_description = db.Column(db.String(120))
    item_weight = db.Column(db.Float)
    item_dimension = db.Column(db.String(120))
    amount = db.Column(db.Float)
    sender_location_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))
    sender_location = db.relationship("Destination", foreign_keys=[sender_location_id])
    note = db.Column(db.String(255))
    traveller_note =db.Column(db.String(255))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    arrival_date = db.Column(db.Date)
    ticket = db.Column(db.String(255))



    def __init__(self, sender_id, destination_id, item_name, item_description, item_weight, item_dimension,sender_location_id,note,start_date,end_date):
        self.sender_id = sender_id
        self.destination_id = destination_id
        self.item_name = item_name
        self.item_description = item_description
        self.item_weight = item_weight
        self.item_dimension = item_dimension
        self.sender_location_id = sender_location_id
        self.note = note
        self.start_date = start_date
        self.end_date = end_date


class Destination(db.Model):
    __tablename__ = 'destinations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    country = db.Column(db.String(80))
    city = db.Column(db.String(80))
    agent_ids =db.Column(db.JSON,nullable=True)
    airport_name = db.Column(db.String(120))
    
    def __init__(self, name, country, city, agent_ids, airport_name):
        self.name = name
        self.country = country
        self.city = city
        self.agent_ids = agent_ids
        self.airport_name = airport_name



class LaundryRequest(db.Model):
    __tablename__ = 'laundryrequests'

    id = db.Column(db.Integer, primary_key=True)
    pickup_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(80))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=[user_id])
    hostel =  db.Column(db.String(80))
    floor   = db.Column(db.String(80))
    room_number = db.Column(db.String(80))
    location = db.Column(db.String(80))
    price = db.Column(db.String(80))
    uid = db.Column(db.String(80))
    note = db.Column(db.String(80))



class PartRequest(db.Model):
    __tablename__ = "partrequests"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=False)
    model_year = db.Column(db.Integer, nullable=False)
    car_make = db.Column(db.String(128), nullable=False)
    car_model = db.Column(db.String(128), nullable=False)
    note = db.Column(db.String(128), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=[user_id])
    status = db.Column(db.String(16), nullable=False)


    def __repr__(self):
        return f'<Part {self.name}>'

class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('partrequests.id'), nullable=False)
    parts = db.relationship("PartRequest", foreign_keys=[part_id])
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vendors  = db.relationship("User", foreign_keys=[vendor_id])
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(16), nullable=False)
    delivery = db.Column(db.String(16), nullable=True)
    note = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<Bid {self.id}>'


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", foreign_keys=[user_id])
    text = db.Column(db.String(255), nullable=True)
    date = db.Column(db.Date)
    vendor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    vendors  = db.relationship("User", foreign_keys=[vendor_id])
    



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
