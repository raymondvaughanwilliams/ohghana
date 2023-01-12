from flask import render_template,request,Blueprint,session,redirect,url_for,jsonify
from structure.models import User,About,Price,Journal,Appointment,Thread,Post
# from structure.team.views import team
# from structure.core.forms import BookingForm,UpdateSessionForm ,JournalForm,Addtherapist
from structure.users.forms import UpdateUserForm
from structure.userportal.forms import BookingForm,UpdateSessionForm ,JournalForm,Addtherapist,SessionForm,AppointmentForm,ContactForm,FeedbackForm,NewThreadForm
from sqlalchemy.orm import load_only
from flask_login import login_required
from structure.models import Appearance,Book
from flask_mail import Mail, Message
from structure import mail,db,app,scheduler
from structure.users.picture_handler import add_profile_pic
from datetime import datetime,timedelta,date
import urllib.request, json 
import random
import string

userportal = Blueprint('userportal',__name__)


 
@userportal.route('/user/dash')
def userdash():
    if session['role'] == 'user':


        user = User.query.filter_by(id=session['id']).first()

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
        
        return render_template('userportal/dashboard.html', user=user,about=about,bookings=bookings,name=name,upcoming=upcomingsessions,previoussessions=previoussessions,therapist=therapist)
    
    else:
        return render_template('error_pages/403.html')
    
    
@userportal.route('/user/uprofile',methods=['GET','POST'])
def uprofile():
    user =User.query.filter_by(id=session['id']).first()

    form = UpdateUserForm()

    if request.method == 'POST':

        if form.picture.data:
            username = user.username
            pic = add_profile_pic(form.picture.data,username)
            user.profile_image = pic

        # user.username = form.username.data
        user.email = form.email.data
        user.name = form.name.data
        user.last_name = form.last_name.data
        user.number = form.number.data
        # user.location = form.location.data
        user.pref_help = form.pref_help.data
        user.pref_therapistgender = form.pref_gender.data
        user.pref_medium = form.pref_medium.data
        print("ao")
        

        db.session.commit()
        return redirect(url_for('userportal.userdash'))

    elif request.method == 'GET':
        form.name.data = user.name
        form.last_name.data = user.last_name
        form.email.data = user.email
        form.number.data = user.number
        form.pref_medium.data = user.pref_medium
        form.pref_help.data = user.pref_help
        form.pref_gender.data= user.pref_therapistgender
        # profile_image = url_for('static', filename='profile_pics/' + user.profile_image)

    return render_template('userportal/profile.html',form=form)


@userportal.route('/user/ujournal')
def ujournal():
    user = User.query.filter_by(email=session['email']).first()
    uid = user.id
    journals = Journal.query.filter_by(user_id =uid)
    return render_template('userportal/journal.html',journals=journals)



@userportal.route('/user/ujournal/<int:id>')
def journaldetails(id):
    journal = Journal.query.filter_by(id=id).first()
    return render_template('userportal/journaldetails.html',journal=journal)



@userportal.route('/user/addujournal',methods=['GET','POST'])
def addujournal():
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
        return redirect(url_for('userportal.ujournal'))  
    return render_template('userportal/addjournal.html',form=form,journals=journals)



@userportal.route('/ujournal/edit/<int:id>', methods=['GET', 'POST'])
def editjournal(id):
    journal = Journal.query.filter_by(id =id).first()
    journals = Journal.query.filter_by(user_id =session['id'])
    text= journal.text
    form = JournalForm()
    if request.method == 'POST':
        journal.text = form.text.data
        journal.title = form.title.data
        db.session.commit()
        return redirect(url_for('userportal.ujournal'))
    elif request.method == 'GET':
        form.title.data = journal.title
        form.text.data = journal.text

  
    return render_template('userportal/editjournal.html',journal=journal,form=form,text=text,journals=journals)





@userportal.route('/user/therapists')
def therapists():
    therapists = User.query.filter_by(role="therapist").all()
    return render_template('userportal/therapists.html',therapists=therapists)



@userportal.route('/user/therapistdetails/<int:id>')
def therapistdetails(id):
    journal = Journal.query.filter_by(id=id).first()
    therapist = User.query.filter_by(id=id).first()
    return render_template('userportal/therapistdetails.html',journal=journal,therapist=therapist)



@userportal.route("/user/book/<int:tid>",methods=['GET', 'POST'])
@login_required
def book(tid):
    form = SessionForm()
    therapist = User.query.filter_by(id=tid).first()
    print(therapist)
    user =  User.query.filter_by(id=session['id']).first()
    tx_ref = user.email[0:6]+ str(random.randint(1,1000))
    tid = tid
    if request.method == 'POST':
        sessions = form.session.data
    else:
        sessions = 1
    markup = 20
    total = int(therapist.baseprice) * int(sessions) + int(markup)
    print('sessions')
    print(sessions)
    return render_template('userportal/bookingdetails.html',total=total,tx_reff=tx_ref,tid=tid,user=user,therapist=therapist,form=form,sessions=sessions)




@userportal.route('/user/appointments')
def appointments():
    user = User.query.filter_by(id=session['id']).first()
    therapist = User.query.filter_by(id=user.therapist_id).first()
    appointments = Appointment.query.filter_by(user_id =session['id'],therapist_id=user.therapist_id).all()
    return render_template('userportal/appointments.html',appointments=appointments,user=user,therapist=therapist)



@userportal.route('/temps')
def temp():
    user = User.query.filter_by(id=session['id']).first()
    
    return render_template('userportal/temp.html')


@userportal.route('/send_message', methods=['POST'])
def send_message():
    print("in")
    message = request.form['message']
    return jsonify({'message': message})

@userportal.route('/temp/<int:thread_id>',methods=['POST','GET'])
def temps(thread_id):
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
        # Create a new post and add it to the databases
        
        post = Post(content=request.form['formcontent'], user_id=session['id'], thread_id=thread.id,main="no")
        db.session.add(post)
        db.session.commit()
        # return redirect(url_for('userportal.view_thread', thread_id=thread.id))
        return jsonify({'posts':posts})

    return render_template('userportal/temp.html',threads=threads, thread=thread, posts=posts,threadform=threadform,user=user,mainpost=mainpost,postlength=postlength)



@userportal.route('/user/addappointment',methods=['GET','POST'])
def addappointment():
    form = AppointmentForm()


    if request.method == 'POST':
        date = form.date.data
        time = form.time.data
        platform = form.platform.data
        user_notes = form.user_notes.data
        user = User.query.filter_by(id=session['id']).first()
        user.rem_sessions = user.rem_sessions - 1
        appointment = Appointment(date=date, time=time, platform=platform,user_confirmation="yes",therapist_confirmation="no",user_id=session['id'],therapist_id=user.therapist_id,user_notes=user_notes)
        db.session.add(appointment)
        db.session.commit()
        print("Appointment Created")  
        return redirect(url_for('userportal.ujournal'))  
    return render_template('userportal/addappointment.html',form=form,)



@userportal.route('/appointment/edit/<int:id>', methods=['GET', 'POST'])
def editappointment(id):
    appointment = Appointment.query.filter_by(id=id).first()
    user = User.query.filter_by(id=session['id']).first()
    appointments = Appointment.query.filter_by(user_id =session['id'],therapist_id=user.therapist_id).all()
    form = AppointmentForm()
    if request.method == 'POST':
        appointment.date = form.date.data
        appointment.time = form.time.data
        appointment.platform = form.platform.data
        appointment.user_notes = form.user_notes.data
        db.session.commit()
        return redirect(url_for('userportal.appointments'))
    elif request.method == 'GET':
        form.date.data = appointment.date
        form.time.data = appointment.time
        form.user_notes.data = appointment.user_notes
        form.platform.data = appointment.platform

  
    return render_template('userportal/editappointment.html',appointment=appointment,form=form,appointments=appointments)



@userportal.route('/user/contact-us',methods=['GET', 'POST'])
def contactus():
    form = ContactForm()
    feedbackform = FeedbackForm()
    if request.method == 'POST':
        print("ajk")
        print(form.hidden.data)
        print(form.name.data)
        if 'hidden' in request.form:
            hidden_value = request.form['hidden']
            name = form.name.data
            text = form.text.data
            email = form.email.data
            
            # Send email using Flask-Mail
            # (Assuming Flask-Mail is configured and imported)
            mail = Mail(app)
            msg = Message('Contact Us Request',
                            sender=email,
                            recipients=['raymondvaughanwilliams@gmail.com'])
            msg.body = f"Name: {name}\nEmail: {email}\nMessage: {text}"
            mail.send(msg)
        else:
            name = form.name.data
            text = form.text.data
            email = form.email.data
            mail = Mail(app)
            msg = Message('Feedback Request',
                            sender=email,
                            recipients=['raymondvaughanwilliams@gmail.com'])
            msg.body = f"Name: {name}\nEmail: {email}\nMessage: {text}"
            mail.send(msg)
            

    return render_template('userportal/contact.html',form=form)



@userportal.route('/userportal/thread/<int:thread_id>',methods=['POST','GET'])
def view_thread(thread_id):
    thread = Thread.query.get(thread_id)
    threads = Thread.query.all()
    mainpost = Post.query.filter(Post.thread_id==thread_id,Post.main=='yes').first()
    posts = thread.posts
    postlength = len(posts)
    threadform = NewThreadForm()
    user = User.query.filter_by(id=session['id']).first()
    
    if request.method == 'POST':
        print("in")
        # Create a new post and add it to the database
        
        post = Post(content=request.form['formcontent'], user_id=session['id'], thread_id=thread.id,main="no")
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('userportal.view_thread', thread_id=thread.id))
        # for post in posts:
        #     if isinstance(post.date, date):
        #         post.date = post.date.isoformat()
        #         print('jhss')
        # return json.dumps([post.__dict__ for post in posts])       
        # return jsonify([post.__dict__ for post in posts])
        # post_list={}
        # for  post in posts:
        #     post_dict= post.__dict__
            
        # return post_list

    return render_template('userportal/thread.html',threads=threads, thread=thread, posts=posts,threadform=threadform,user=user,mainpost=mainpost,postlength=postlength)



# @userportal.route('/thread/new', methods=['GET', 'POST'])
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

# @userportal.route('/thread/<int:thread_id>/reply', methods=['GET', 'POST'])
# def reply(thread_id):
#     thread = Thread.query.get(thread_id)
#     if request.method == 'POST':
#         # Create a new post and add it to the database
#         user = User.query.filter_by(id=session['id']).first()
#         post = Post(content=request.form['content'], user=user, thread=thread)
#         db.session.add(post)
#         db.session.commit()
#         return redirect(url_for('userportal.view_thread', thread_id=thread.id))

#     else:
#         # Render the form for creating a reply
#         return render_template('reply.html', thread=thread)


@userportal.route('/user/discussionforum',methods=['GET', 'POST'])
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
    return render_template('userportal/discussionforum.html', threads=threads,threadform=threadform)


@userportal.route("/create_meeting")
def create_meeting():
    # Generate a random room name
    room_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return render_template("userportal/jitsi_template.html", room_name=room_name)




def create_meeting_link_task(appointment_id):
    # Get the appointment details
    appointment = Appointment.query.filter_by(id=appointment_id)
    start_time = datetime.datetime.strptime(appointment.date + " " + appointment.time, "%Y-%m-%d %H:%M:%S")
    start_time = start_time - datetime.timedelta(minutes=15)
    end_time = start_time + datetime.timedelta(hours=1)

    # Generate a random room name
    room_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

    # Create the meeting link with start time and end time
    meeting_link = f"https://meet.jit.si/{room_name}?start={start_time.strftime('%s')}&end={end_time.strftime('%s')}"
    print("meeting link")
    print(meeting_link)
    appointment.therapist_confirmation = "yes"
    appointment.meeting_link = meeting_link
    db.session.commit()
    # Send the meeting link to the attendees via email or messaging service
    # send_invite(meeting_link, appointment.attendees)

@app.route('/schedule_meeting/<appointment_id>')
def schedule_meeting(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id)
    start_time = datetime.datetime.strptime(appointment.date + " " + appointment.time, "%Y-%m-%d %H:%M:%S")
    start_time = start_time - datetime.timedelta(minutes=15)

    # Schedule the task to run 15 minutes before the appointment date and time
    scheduler.add_job(func=create_meeting_link_task, trigger='date', run_date=start_time, args=[appointment_id])
    scheduler.start()
    return jsonify({"message": "Meeting link scheduled"})

