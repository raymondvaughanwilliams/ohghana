from flask import render_template,request,Blueprint,session,redirect,url_for,jsonify
from structure.models import User,About,Bid,PartRequest,Farmer,EcomRequest
# from structure.team.views import team
from structure.core.forms import DeliveryForm, FilterForm,ContactForm,AcceptBidForm

from sqlalchemy.orm import load_only
from flask_login import login_required

from structure.users.forms import LoginForm, UpdateAgentForm
from flask_mail import Mail, Message
from structure import mail,db,app
from datetime import datetime,timedelta
import urllib.request, json
import random
import string
from structure.users.picture_handler import add_profile_pic
from sqlalchemy import  and_, or_ ,desc ,asc 


therapistportal = Blueprint('therapistportal',__name__)






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



@therapistportal.route('/agent/dash')
def agent_dashboard():
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)
    
    farmers = Farmer.query.all()
    
    form = FilterForm()
    if session['role'] == 'agent':

        deliveries = Bid.query.filter_by(delivery='needpartsdelivery',status='accepted').all()
        print(deliveries)


        name = user.name
        # print(op)

        return render_template('agentportal/dashboard.html',form=form, user=user,about=about,name=name,deliveries=deliveries,farmers=farmers)
 
        
    # return render_template('agentportal/dashboard.html',form=form, user=user,about=about,name=user.name,pendingdeliveries=pendingdeliveries,confirmeddeliveries=confirmeddeliveries,completeddeliveries=completeddeliveries,claimeddeliveries=claimeddeliveries)
 

 
@therapistportal.route("/deliveries/<int:package_id>", methods=["GET", "POST"])
def update_package(package_id):
    form = AcceptBidForm()
    # destinations = Destination.query.all()
    
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
 

    return render_template("agentportal/confirmdelivery.html", delivery=delivery,form=form)



@therapistportal.route('/agent/packages',methods=['GET', 'POST'])
def packages():
    filterform = FilterForm()
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)

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




@therapistportal.route('/api2/checknumber',methods=['GET','POST'])
# @jwt_required()
def checknumber():
     
    # print(request.args.get('number'))

    # number = requests.json['number'] 
    number = request.args.get('number')
 
    farmer = Farmer.query.filter_by(number=number).first()
    if farmer is not None:
        
        ecomrequest =  EcomRequest(number=number,country=farmer.country,farmer_id=farmer.id,cash_code=farmer.cash_code)
        db.session.add(ecomrequest)
        db.session.commit()

        payload = {"firstName":farmer.first_name,
        "lastName":farmer.last_name,
        "premium_amount":farmer.premium_amount,
        "location":farmer.location
        }
        context = {"status" :True,
    "message" : " Farmer found",
        "data" : payload
        }
        return jsonify(context)
    else:
        context = {"status" :False,
        "message":"Farmer not found",
        "error": "null"}
        return jsonify(context)
    