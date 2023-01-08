from flask import render_template,request,Blueprint,session,redirect,url_for,jsonify
from structure.models import User,About,Price, WebFeature,Faq,Testimonial,Team,Appearance,Block,Journal ,Payment,NewsletterContacts,Appointment,Thread,Post
# from structure.team.views import team
from structure.core.forms import BookingForm,UpdateSessionForm ,JournalForm,Addtherapist ,NewsletterForm
from structure.userportal.forms import ContactForm,AppointmentForm,NewThreadForm
from sqlalchemy.orm import load_only
from flask_login import login_required
from structure.appearance.forms import AppearanceForm
from structure.block.forms import BlockForm
from structure.users.forms import LoginForm, UpdateTherapistForm
from structure.appearance.views import appearance
from structure.models import Appearance,Book
from flask_mail import Mail, Message
from structure import mail,db,app
from datetime import datetime,timedelta
import urllib.request, json
import random
from structure.users.picture_handler import add_profile_pic


therapistportal = Blueprint('therapistportal',__name__)

@therapistportal.route('/therapist/dashboard')
def therapistdash():
    form = AppointmentForm()
    if session['role'] == 'therapist':


        user = User.query.filter_by(id=session['id']).first()
        # upcomingappointments = Appointment.query.filter(Appointment.date > datetime.now()).filter(Appointment.therapist_id == user.id).all()
        upcomingappointments = Appointment.query.filter(Appointment.date > datetime.now()).filter(Appointment.therapist_id == user.id).filter(Appointment.therapist_confirmation == "yes").filter(Appointment.user_confirmation == "yes").all()
        confirmappointments = Appointment.query.filter(Appointment.date > datetime.now()).filter(Appointment.therapist_id == user.id).filter(Appointment.therapist_confirmation == "no").filter(Appointment.user_confirmation == "yes").all()
        rescheduledappointments = Appointment.query.filter(Appointment.date > datetime.now()).filter(Appointment.therapist_id == user.id).filter(Appointment.therapist_confirmation == "yes").filter(Appointment.user_confirmation == "no").all()
        print(upcomingappointments)
        about = About.query.get(1)
        # op = user.plan_id
        bookings = Book.query.filter_by(email=session["email"]).all()
        todaysdate = datetime.now() 
        therapist = User.query.filter_by(id=user.therapist_id).first()
        # current_therapist = User.query.filter_by(id=user.therapist_id).first()
        print("todaysdate")
        print(todaysdate)
        upcomingsessions ={}
        previoussessions = {}
        for booking in bookings:
            if booking.date > todaysdate:
                # upcomingsessions.append(booking.webfeatures.title)
                upcomingsessions[booking.id] = booking.webfeatures.title
                # print(upcomingsessions)
            else:
                previoussessions[booking.id] = booking.webfeatures.title
        sesh = Book.query.get(8)

        name = user.name
        # print(op)

        # print(comment.user.title)
        therapist_ids = []
        therapistss = {}
        for booking in bookings:
            # therapistss.append(booking.webfeatures.title)
            therapistss[booking.id] = booking.webfeatures.title
        # plan = Price.query.filter_by(id=op).first()
        # print(plan)
        
        return render_template('therapistportal/dashboard.html',form=form, user=user,about=about,bookings=bookings,name=name,upcoming=upcomingsessions,previoussessions=previoussessions,therapist=therapist,upcomingappointments=upcomingappointments,confirmappointments=confirmappointments,rescheduledappointments=rescheduledappointments)
    
    else:
        return render_template('error_pages/403.html')



@therapistportal.route("/confirmappointment/<int:appointment_id>",methods=["POST"])
@login_required
def confirmappointment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if request.method == "POST":
        appointment.therapist_confirmation = "yes"
        db.session.commit()
        return redirect(url_for('therapistportal.therapistdash'))
        

@therapistportal.route("/editappointment/<int:appointment_id>",methods=["POST","GET"])
@login_required
def editappointment(appointment_id):
    form = AppointmentForm()
    user = User.query.filter_by(id=session['id']).first()
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if request.method == "POST":
        appointment.therapist_confirmation = "yes"
        appointment.user_confirmation = "no"
        appointment.date = form.date.data 
        appointment.time = form.time.data
        appointment.therapist_notes = form.therapist_notes.data
        appointment.platform = form.platform.data
        db.session.commit()
        return redirect(url_for('therapistportal.therapistdash'))
    elif request.method == 'GET':
        form.date.data = appointment.date
        form.time.data = appointment.time
        form.therapist_notes.data = appointment.therapist_notes
        form.platform.data = appointment.platform
    return render_template('therapistportal/editappointment.html',form=form)
        
        
        
@therapistportal.route('/therapist/tjournal')
def tjournal():
    user = User.query.filter_by(email=session['email']).first()
    uid = user.id
    journals = Journal.query.filter_by(user_id =uid)
    return render_template('therapistportal/journal.html',journals=journals)



@therapistportal.route('/therapist/tjournal/<int:id>')
def journaldetails(id):
    journal = Journal.query.filter_by(id=id).first()
    return render_template('therapistportal/journaldetails.html',journal=journal)



@therapistportal.route('/therapist/addtjournal',methods=['GET','POST'])
def addtjournal():
    form = JournalForm()
    journals = Journal.query.filter_by(user_id =session['id']).all()

    if request.method == 'POST':
        title = form.title.data
        text = form.text.data
        useremail = session['email']
        user = User.query.filter_by(email=useremail).first()
        uid = user.id
        journal = Journal(title=title,
                             text=text,
                             user_id=uid
                             )
        db.session.add(journal)
        db.session.commit()
        print("Journal Created")  
        return redirect(url_for('therapistportal.tjournal'))  
    return render_template('userportal/addjournal.html',form=form,journals=journals)



@therapistportal.route('/therapist/tjournal/edit/<int:id>', methods=['GET', 'POST'])
def editjournal(id):
    journal = Journal.query.filter_by(id =id).first()
    journals = Journal.query.filter_by(user_id =session['id'])
    text= journal.text
    form = JournalForm()
    if request.method == 'POST':
        journal.text = form.text.data
        journal.title = form.title.data
        db.session.commit()
        return redirect(url_for('therapistportal.tjournal'))
    elif request.method == 'GET':
        form.title.data = journal.title
        form.text.data = journal.text

  
    return render_template('therapistportal/editjournal.html',journal=journal,form=form,text=text,journals=journals)



@therapistportal.route('/therapist/profile',methods=['GET','POST'])
def tprofile():
    user =User.query.filter_by(id=session['id']).first()

    form = UpdateTherapistForm()

    if request.method == 'POST':

        # if form.picture.data:
        #     username = user.username
        #     pic = add_profile_pic(form.picture.data,username)
        #     user.profile_image = pic

        # user.username = form.username.data
        user.email = form.email.data
        user.name = form.name.data
        user.last_name = form.last_name.data
        user.number = form.number.data
        user.picture  = form.picture.data
        user.location = form.location.data
        user.specialty = form.specialty.data
        user.biography = form.biography.data
        user.years_of_experience = form.experience.data
        user.baseprice = form.baseprice.data
        user.platforms = form.platform.data
        print("ao")
        db.session.commit()
        
        return redirect(url_for('therapistportal.tprofile'))
    elif request.method == 'GET':
        form.name.data = user.name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.number.data = user.number
        form.location.data = user.location
        form.specialty.data = user.specialty
        form.biography.data = user.biography
        form.experience.data = user.years_of_experience
        form.baseprice.data = user.baseprice
        form.platform.data = user.platforms
        

        db.session.commit()
        
    return render_template('therapistportal/profile.html',form=form)



@therapistportal.route('/therapistportal/thread/<int:thread_id>',methods=['POST','GET'])
def view_thread(thread_id):
    thread = Thread.query.get(thread_id)
    threads = Thread.query.all()
    mainpost = Post.query.filter(Post.thread_id==thread_id,Post.main=='yes').first()
    print('thread')
    print(thread)
    posts = thread.posts
    postlength = len(posts)
    print(postlength)
    threadform = NewThreadForm()
    user = User.query.filter_by(id=session['id']).first()
    
    if request.method == 'POST':
        # Create a new post and add it to the database
        
        post = Post(content=request.form['content'], user_id=session['id'], thread_id=thread.id,main="no")
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('therapistportal.view_thread', thread_id=thread.id))

    return render_template('therapistportal/thread.html',threads=threads, thread=thread, posts=posts,threadform=threadform,user=user,mainpost=mainpost,postlength=postlength)



# @therapistportal.route('/thread/new', methods=['GET', 'POST'])
# def new_thread():
#     if request.method == 'POST':
#         # Create a new thread and add it to the database
#         user = User.query.filter_by(id=session['id']).first()
#         thread = Thread(title=request.form['title'], user=user)
#         db.session.add(thread)
#         db.session.commit()
#         return redirect(url_for('view_thread', thread_id=thread.id))
        
#     else:
#         # Render the form for creating a new thread
#         return render_template('new_thread.html')

@therapistportal.route('/thread/<int:thread_id>/reply', methods=['GET', 'POST'])
def reply(thread_id):
    thread = Thread.query.get(thread_id)
    if request.method == 'POST':
        # Create a new post and add it to the database
        user = User.query.filter_by(id=session['id']).first()
        post = Post(content=request.form['content'], user=user, thread=thread)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('therapistportal.view_thread', thread_id=thread.id))

    else:
        # Render the form for creating a reply
        return render_template('reply.html', thread=thread)


@therapistportal.route('/user/discussionforum',methods=['GET', 'POST'])
def discussionforum():
    threads = Thread.query.all()
    threadform = NewThreadForm()
    if request.method == 'POST':
        thread = Thread(title=threadform.title.data,user_id=session['id'],anonymous=threadform.anonymous.data)
        db.session.add(thread)
        db.session.commit()
        print("t")
        thread_id = thread.id
        content = threadform.content.data
        post = Post(content=content,thread_id=thread_id,user_id=session['id'],main='yes')
        db.session.add(post)
        db.session.commit()
    return render_template('therapistportal/discussionforum.html', threads=threads,threadform=threadform)