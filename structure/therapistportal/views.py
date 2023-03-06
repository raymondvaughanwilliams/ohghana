from flask import render_template,request,Blueprint,session,redirect,url_for,jsonify
from structure.models import User,About,Price, WebFeature,Faq,Testimonial,Team,Appearance,Block,Journal ,Payment,NewsletterContacts,Appointment,Thread,Post ,Note,Delivery,Destination,Bid,PartRequest
# from structure.team.views import team
from structure.core.forms import BookingForm,UpdateSessionForm ,JournalForm,Addtherapist ,NewsletterForm,DeliveryForm, FilterForm,ContactForm,AcceptBidForm

from structure.userportal.forms import AppointmentForm,NewThreadForm,NotesForm
from sqlalchemy.orm import load_only
from flask_login import login_required
from structure.appearance.forms import AppearanceForm
from structure.block.forms import BlockForm
from structure.users.forms import LoginForm, UpdateAgentForm
from structure.appearance.views import appearance
from structure.models import Appearance,Book
from flask_mail import Mail, Message
from structure import mail,db,app,scheduler
from datetime import datetime,timedelta
import urllib.request, json
import random
import string
from structure.users.picture_handler import add_profile_pic
from sqlalchemy import  and_, or_ ,desc ,asc 


therapistportal = Blueprint('therapistportal',__name__)





# def create_meeting_link_task(appointment_id):
#     # Get the appointment details
#     appointment = Appointment.query.filter_by(id=appointment_id)
#     start_time = datetime.strptime(appointment.date + " " + appointment.time, "%Y-%m-%d %H:%M:%S")
#     start_time = start_time - datetime.timedelta(minutes=15)
#     end_time = start_time + datetime.timedelta(hours=1)

#     # Generate a random room name
#     room_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

#     # Create the meeting link with start time and end time
#     meeting_link = f"https://meet.jit.si/{room_name}?start={start_time.strftime('%s')}&end={end_time.strftime('%s')}"
#     print("meeting link")
#     print(meeting_link)
#     appointment.therapist_confirmation = "yes"
#     appointment.meeting_link = meeting_link
#     db.session.commit()
#     return render_template("userportal/jitsi_template.html", meeting_link=meeting_link)
#     # Send the meeting link to the attendees via email or messaging service
#     # send_invite(meeting_link, appointment.attendees)






@therapistportal.route('/therapist/dashboard')
def therapistdash():
    form = AppointmentForm()
    if session['role'] == 'agent':
        deliveries = Bid.query.filter_by(delivery='needpartsdelivery',status='claimed').first()


        user = User.query.filter_by(id=session['id']).first()
        # upcomingappointments = Appointment.query.filter(Appointment.date > datetime.now()).filter(Appointment.therapist_id == user.id).all()
       
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
        
        return render_template('therapistportal/dashboard.html',form=form, user=user,about=about,bookings=bookings,name=name,upcoming=upcomingsessions,previoussessions=previoussessions,therapist=therapist,deliveries=deliveries)
    
    else:
        return render_template('error_pages/403.html')



@therapistportal.route("/confirmappointment/<int:appointment_id>",methods=["POST"])
@login_required
def confirmappointment(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    if request.method == "POST":
        # appointment.therapist_confirmation = "yes"
        start_time = datetime.strptime(str(appointment.date) + " " + str(appointment.time), "%Y-%m-%d %H:%M:%S")
        start_time = start_time - timedelta(minutes=15)
        end_time = start_time + timedelta(hours=1)
        rand_id=''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        # Generate a random room name
        room_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))

        # Create the meeting link with start time and end time
        meeting_link = f"https://meet.jit.si/{room_name}?start={start_time.strftime('%s')}&end={end_time.strftime('%s')}"
        print("meeting link")
        print(meeting_link)
        
        appointment.therapist_confirmation = "yes"
        appointment.meeting_link = meeting_link
        # scheduler.add_job(func=create_meeting_link_task, trigger='date', run_date=start_time, args=[appointment_id],id=rand_id)
        # scheduler.start()
        db.session.commit()
        return redirect(url_for('therapistportal.therapistdash'))

        
@therapistportal.route("/room/<int:appointment_id>")
def appointment_room(appointment_id):
    appointment = Appointment.query.filter_by(id=appointment_id).first()
    # Generate a random room name
    form = NotesForm()
    room_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return render_template("therapistportal/meetingroom.html",meeting_link=appointment.meeting_link ,form=form,appointment_id=appointment_id)

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


@therapistportal.route("/save_therapistnote", methods=["POST"])
def save_therapistnote():
    if request.method == 'POST':
        data = request.get_json()
        note_content = data["content"]
        appointment_id = data["appointment_id"]
        existing_note = Note.query.filter_by(appointment_id=appointment_id).first()

    if existing_note:
        print("en")
        # Update the existing note
        existing_note.text = note_content
        db.session.commit()
        return jsonify({"message": "Note updated successfully!"})
    else:
        print("no")
        # Create a new note
        note = Note(text=data["content"],user_id=session['id'],therapist_id=session['id'] ,appointment_id=data["appointment_id"])
        db.session.add(note)
        db.session.commit()
        return jsonify({"message": "Note saved successfully!"})

        # if len(note>0):
        #     existing_note.text = data["content"]
        #     db.session.commit()
        #     return jsonify({"message": "Note updated successfully!"})
            
        # data = request.get_json()
        # print("in")
        # print(data)
        # note = Note(text=data["content"],user_id=session['id'],therapist_id=session['id'])
        # db.session.add(note)
        # db.session.commit()
        # return jsonify({"message": "Note saved successfully!"})

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



@therapistportal.route('/agent/dashboard')
def agent_dashboard():
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)

    form = AppointmentForm()
    if session['role'] == 'agent':

        deliveries = Bid.query.filter_by(delivery='needpartsdelivery',status='accepted').all()
        print(deliveries)
       
        # upcomingappointments = Appointment.query.filter(Appointment.date > datetime.now()).filter(Appointment.therapist_id == user.id).all()
        about = About.query.get(1)
        # op = user.plan_id
        todaysdate = datetime.now() 
        # current_therapist = User.query.filter_by(id=user.therapist_id).first()
        # print("todaysdate")
        # print(todaysdate)
        upcomingsessions ={}
        previoussessions = {}
      

        name = user.name
        # print(op)

        return render_template('agentportal/dashboard.html',form=form, user=user,about=about,name=name,upcoming=upcomingsessions,deliveries=deliveries)
 
        
    # return render_template('agentportal/dashboard.html',form=form, user=user,about=about,name=user.name,pendingdeliveries=pendingdeliveries,confirmeddeliveries=confirmeddeliveries,completeddeliveries=completeddeliveries,claimeddeliveries=claimeddeliveries)
 
 
 
@therapistportal.route("/deliveries/<int:package_id>", methods=["GET", "POST"])
def update_package(package_id):
    form = AcceptBidForm()
    destinations = Destination.query.all()
    
    delivery = Bid.query.get(package_id)
    part = PartRequest.query.filter_by(id=delivery.part_id).first()
    
    if not delivery:
        return render_template("error.html", message="Delivery not found"), 404
    if request.method == "POST":
        if form.status.data == 'denied':
            status = 'pending'
        else:
            status = form.status.data

        delivery.note = form.note.data
        delivery.status = form.deliverystatus.data
        part.status=form.deliverystatus.data

        
        db.session.commit()
        return redirect(url_for("therapistportal.agent_dashboard"))
    elif request.method == 'GET':
        form.status.data = delivery.status
        form.note.data = delivery.note
 

    return render_template("agentportal/confirmdelivery.html", delivery=delivery,form=form,destinations=destinations)



@therapistportal.route('/agent/packages',methods=['GET', 'POST'])
def packages():
    filterform = FilterForm()
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)
    packages = Delivery.query.filter_by(destination_id = user.location_id).all()
    destinations = Destination.query.all()
    if request.method == "POST":
        # Get the filter values from the form
        traveler_email = filterform.traveller.data
        sender_email= filterform.sender.data
        location = filterform.location.data
        destination = filterform.destination.data
        status = filterform.status.data
        date_min = filterform.start_date.data
        date_max = filterform.end_date.data
        # Build the SQLAlchemy filter conditions
        conditions = []
        if traveler_email:
            conditions.append(Delivery.traveler.email == traveler_email)
        if sender_email:
            conditions.append(Delivery.sender.email == sender_email)
        if location:
            # Build a list of conditions that match the location field
            # using the LIKE operator and the % wildcard
            location_conditions = [
                Delivery.sender_location_id.like(f"%{location}%"),
                Delivery.sender_location_id.like(f"{location}%"),
                Delivery.sender_location_id.like(f"%{location}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*location_conditions))
        if destination:
            # Build a list of conditions that match the destination field
            # using the LIKE operator and the % wildcard
            destination_conditions = [
                Delivery.destination_id.like(f"%{destination}%"),
                Delivery.destination_id.like(f"{destination}%"),
                Delivery.destination_id.like(f"%{destination}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the destination variations
            conditions.append(or_(*destination_conditions))
        if status and status != "all":
            conditions.append(Delivery.delivery_status == status)
        if date_min and date_max:
            # Filter for Deliverys with dates within the specified range
            conditions.append(and_(Delivery.start_date >= date_min, Delivery.end_date <= date_max))
        elif date_min:
            # Filter for Deliverys with dates greater than or equal to the specified minimum
            conditions.append(Delivery.start_date >= date_min)
        elif date_max:
            # Filter for Deliverys with dates less than or equal to the specified maximum
            conditions.append(Delivery.end_date <= date_max)

        # Filter the Deliverys based on the conditions
        print(conditions[0])
        packages = Delivery.query.filter(and_(*conditions)).all()
        return render_template("agentportal/packages.html", packages=packages,user=user,filterform=filterform,destinations=destinations)
    return render_template("agentportal/packages.html", packages=packages,user=user,filterform=filterform,destinations=destinations)




@therapistportal.route("/agent/packages/new", methods=["GET", "POST"])
def new_package():
    form = DeliveryForm()
    user  = User.query.filter_by(id=session['id']).first()
    destinations  = Destination.query.all()
    if request.method == "POST":
        # destination = Destination.query.filter_by(name=request.form["destination"]).first()
        # if not destination:
        #     return render_template("create_delivery.html", error="destination not found")
        print("dates")
        print(form.start_date.data)
        print(form.end_date.data)
        delivery = Delivery(sender_id=session['id'], destination_id=form.destination.data, sender_location_id=user.location.id,item_name=form.item_name.data,item_description= form.item_description.data,item_weight=form.item_weight.data, item_dimension=form.item_dimension.data,note=form.note.data,start_date=form.start_date.data,end_date=form.end_date.data)
        db.session.add(delivery)
        db.session.commit()
        return redirect(url_for("therapistportal.agent_dashboard"))
    return render_template("agentportal/new_delivery.html",form=form,destinations=destinations)



@therapistportal.route('/user/profile',methods=['GET','POST'])
def profile():
    user =User.query.filter_by(id=session['id']).first()

    form = UpdateAgentForm()

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

    return render_template('agentportal/profile.html',form=form)



@therapistportal.route('/agent/contact-us',methods=['GET', 'POST'])
def contactus():
    form = ContactForm()
    feedbackform = ContactForm()
    if form.email.data:
        sender = form.email.data
    else:
        sender ="pquinton10@gmail.com"
    if request.method == 'POST':
        print("ajk")
        print(form.hidden.data)
        print(form.name.data)
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
        name = form.name.data
        text = form.text.data
        email = form.email.data
        mail = Mail(app)
        msg = Message('Feedback Request',
                        sender=email,
                        recipients=['raymondvaughanwilliams@gmail.com'])
        msg.body = f"Name: {name}\nEmail: {email}\nMessage: {text}"
        mail.send(msg)
            

    return render_template('agentportal/contact.html',form=form)