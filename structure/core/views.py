from flask import render_template,Blueprint,session,redirect,url_for,jsonify,current_app,request
from structure.models import User,About,Faq,Testimonial,PartRequest,Bid,Review,Farmer,EcomRequest
# from structure.team.views import team

from structure.about.forms import AboutForm
from structure.core.forms import FilterForm,RequestForm,BidForm,AcceptBidForm,ReviewForm,FarmerForm
from sqlalchemy.orm import load_only
from flask_login import login_required
from flask_mail import Mail, Message
from structure import mail,db,photos
from datetime import datetime,timedelta
import secrets
import requests
import csv
import os
from sqlalchemy import  and_, or_ ,desc ,asc 
from os import environ


core = Blueprint('core',__name__)

API_KEY = os.environ.get('API_KEY')

def require_api_key(view_function):
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid API key'}), 401
    return decorated_function


@core.route('/base')
def base():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    about = About.query.all()
    return render_template('base.html',about=about)


@core.route('/h',methods=['GET', 'POST'])
def inp_home():
    aboutform = AboutForm()

    page = request.args.get('page', 1, type=int)

    about = About.query.get(1)
    faq = Faq.query.all()
    testimonial = Testimonial.query.all()


    partrequests = PartRequest.query.filter_by(status="requested").all()
    print(partrequests)
    
    
    therapistobj = User.query.filter_by(role="therapist").all()
    
    # if request.method == "POST":
    #     name = newsletterform.name.data
    #     phone = newsletterform.phone.data
    #     email = newsletterform.email.data
    #     contact = NewsletterContacts(name = name, phone = phone, email = email)
    #     db.session.add(contact)
    #     db.session.commit()
    # teammateform = Team()
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('website/index.html',partrequests =partrequests, form=aboutform)


@core.route("/request/newpart", methods=["GET", "POST"])
def new_request():
    form = RequestForm()
    items  = PartRequest.query.all()
    if request.method == "POST":
        # destination = Destination.query.filter_by(name=request.form["destination"]).first()
        # if not destination:
        #     return render_template("create_PartRequest.html", error="destination not found")
  
        partrequest = PartRequest(user_id=session['id'], name=form.name.data, description=form.description.data,model_year=form.model_year.data,status= "requested",car_make=form.car_make.data, car_model=form.car_model.data,quantity=form.quantity.data,note=form.note.data)
        db.session.add(partrequest)
        db.session.commit()
        return redirect(url_for("core.myrequests"))
    return render_template("portal/newrequest.html",form=form,items=items)



@core.route('/request/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def updaterequest(id):
    # user = User.query.filter_by(email=session['email']).first()
    # uid = user.id
    partrequest = PartRequest.query.filter_by(id=id).first()
    form = RequestForm()

            # user = User.query.filter_by(email=form.email.data).first()
    if request.method == 'POST':

        
        partrequest.name = form.name.data
        partrequest.description = form.description.data
        partrequest.car_make = form.car_make.data
        partrequest.car_model = form.car_model.data
        partrequest.quantity = form.quantity.data
        partrequest.note = form.note.data

        db.session.commit()
        return redirect(url_for('core.myrequests'))
    
    elif request.method == 'GET':
        form.name.data = partrequest.name
        form.description.data = partrequest.description
        form.car_make.data = partrequest.car_make
        form.car_model.data = partrequest.car_model
        form.quantity.data = partrequest.quantity
        form.note.data = partrequest.note
  
    return render_template('portal/updatepartrequest.html',form=form)




@core.route("/<int:part_id>/bid", methods=["GET", "POST"])
def bid(part_id):
    form = BidForm()
    partrequest = PartRequest.query.get(part_id)
    if not partrequest:
        return render_template("error.html", message="Delivery not found"), 404
    if request.method == "POST":
        if request.files.get('image'):
            image1 = photos.save(request.files['image'], name=secrets.token_hex(10) + ".")
            image1= "static/images/tickets/"+image1
        else:
            image1 = "static/images/noimage.JPG"   
        print("bidding") 
        bid= Bid(part_id=part_id, vendor_id=session['id'],quantity=form.quantity.data,price=form.price.data,status="bid")
        db.session.add(bid)
        db.session.commit()
        return redirect(url_for("core.inp_home"))

        
    return render_template("portal/bid.html", partrequest=partrequest,form=form)


@core.route("/myrequests", methods=["GET"])
def myrequests():
    partrequests = PartRequest.query.filter((PartRequest.user_id==session['id'])).all()
    print ("deliveries")
    print(partrequests)
    user = User.query.filter_by(id=session['id']).first()
    print(user)

    return render_template("portal/mypartrequests.html", partrequests=partrequests,user=user)


@core.route("/mybids", methods=["GET"])
def mybids():
    bids = Bid.query.filter((Bid.vendor_id==session['id'])).all()
    print ("deliveries")
    print(bids)
    user = User.query.filter_by(id=session['id']).first()
    print(user)

    return render_template("portal/mybids.html", bids=bids,user=user)


@core.route("/bids/<int:part_id>", methods=["GET"])
def bids(part_id):
    bids = Bid.query.filter_by(part_id=part_id).all()
    print ("deliveries")
    print(bids)
    user = User.query.filter_by(id=session['id']).first()
    print(user)

    return render_template("portal/bids.html", bids=bids,user=user)


@core.route("/viewbid/<int:bid_id>", methods=["POST",'GET'])
def viewbid(bid_id):
    form = AcceptBidForm()
    bid = Bid.query.filter_by(id=bid_id).first()
    bids = Bid.query.filter_by(part_id=bid.part_id).all()
    print(bid)
    partrequest = PartRequest.query.filter_by(id=bid.part_id).first()
    user = User.query.filter_by(id=session['id']).first()
    if bid.status == 'standard':
        bidaccepted = True
    else:
        bidaccepted = False
    message = False
    if bid.status == 'accepted':
        bidaccepted = True
    else:
        bidaccepted = False
    print(user)
    if request.method == "POST":
        bid.status = form.status.data
        bid.delivery = form.delivery.data
        partrequest.set_status="claimed"
        db.session.commit()
        for ubid in bids:
            if bid.status=="accepted" and ubid.id != bid.id  :
                ubid.status = "denied"
                db.session.commit()
        if form.delivery.data  == 'standard':
            message=  True
        else:
            message= False
        return redirect(url_for("core.inp_home"))
    

                

    return render_template("portal/viewbid.html", bids=bid,user=user,partrequest=partrequest,form=form,bidaccepted=bidaccepted,message=message)



@core.route("/viewmybid/<int:bid_id>", methods=["POST",'GET'])
def viewmybid(bid_id):
    form = BidForm()
    bid = Bid.query.filter_by(id=bid_id).first()
    bids = Bid.query.filter_by(part_id=bid.part_id).all()
    print(bid)
    partrequest = PartRequest.query.filter_by(id=bid.part_id).first()
    user = User.query.filter_by(id=session['id']).first()
    
    print(user)
    if request.method == "POST":
        bid.price = form.price.data
        bid.quantity = form.quantity.data
        # bid.status = 'bid'
        
        db.session.commit()
        
    
        return redirect(url_for("core.inp_home"))
    
    elif request.method == 'GET':
        form.price.data = bid.price
        form.quantity.data = bid.quantity
        
    return render_template("portal/viewmybid.html", bids=bid,user=user,partrequest=partrequest,form=form)



@core.route("/vendor/<int:vendor_id>", methods=["GET","POST"])
def vendor(vendor_id):
    form = ReviewForm()
    vendor = User.query.filter_by(id=vendor_id).first()

    user = User.query.filter_by(id=session['id']).first()
    print(user)
    parts = vendor.parts.split(",")
    print(parts)
    vendorparts = []
    for item in parts:
        vendorparts.append(item)
    print(vendorparts)
    cars = vendor.cars.split(",")
    print(cars)
    vendorcars = []
    for car in cars:
        vendorcars.append(car)
    print(vendorcars)
    bids = Bid.query.filter_by(vendor_id=vendor_id).all()
    successfulsales =  len(Bid.query.filter_by(vendor_id=vendor_id,status='delivered').all())
    allsales = len(Bid.query.filter_by(vendor_id=vendor_id).all())
    sales = Bid.query.filter_by(vendor_id=vendor_id).all()
    reviews = Review.query.filter_by(vendor_id=vendor_id).all()
    
    
    if request.method == 'POST':
        review = Review(user_id = user.id , text = form.text.data,date=datetime.now(),vendor_id=vendor_id)
        db.session.add(review)
        db.session.commit()
    
        

    return render_template("portal/vendor.html", vendor=vendor,user=user,vendorparts=vendorparts,vendorcars=vendorcars,bids=bids,allsales =allsales ,successfulsales=successfulsales,reviews=reviews,form=form)


@core.route('/agent/dashboard')
def agent_dashboard():
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)
    
    farmers = Farmer.query.all()
    ecomrequests  = EcomRequest.query.all()
    
    form = FilterForm()
    if session['role'] == 'agent':

        deliveries = Bid.query.filter_by(delivery='needpartsdelivery',status='accepted').all()
        print(deliveries)


        name = user.name
        # print(op)

    return render_template('agentportal/dashboard.html',form=form, user=user,about=about,name=name,deliveries=deliveries,farmers=farmers,ecomrequests=ecomrequests)



@core.route('/claims', methods=['GET', 'POST'])
def claims():
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)
    

    ecomrequests  = EcomRequest.query.all()
    
    form = FilterForm()


    deliveries = Bid.query.filter_by(delivery='needpartsdelivery',status='accepted').all()
    print(deliveries)


    name = user.name
    
    
    if request.method == "POST":
        # Get the filter values from the form
        first_name = form.first_name.data
        print (first_name)
        last_name= form.last_name.data
        location = form.location.data
        number = form.number.data

        # Build the SQLAlchemy filter conditions
        conditions = []
        if first_name:
            conditions.append(EcomRequest.farmers.first_name == first_name)
        if last_name:
            conditions.append(EcomRequest.farmers.last_name == last_name)
        if number:
            # Build a list of conditions that match the location field
            # using the LIKE operator and the % wildcard
            number_conditions = [
                EcomRequest.number.like(f"%{number}%"),
                EcomRequest.number.like(f"{number}%"),
                EcomRequest.number.like(f"%{number}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*number_conditions))
        if location:
            # Build a list of conditions that match the destination field
            # using the LIKE operator and the % wildcard
            location_conditions = [
                EcomRequest.farmers.location.like(f"%{location}%"),
                EcomRequest.farmers.like(f"{location}%"),
                EcomRequest.farmers.like(f"%{location}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the destination variations
            conditions.append(or_(*location_conditions))
        # if status and status != "all":
        #     conditions.append(Delivery.delivery_status == status)
        # if date_min and date_max:
        #     # Filter for Deliverys with dates within the specified range
        #     conditions.append(and_(Delivery.start_date >= date_min, Delivery.end_date <= date_max))
        # elif date_min:
        #     # Filter for Deliverys with dates greater than or equal to the specified minimum
        #     conditions.append(Delivery.start_date >= date_min)
        # elif date_max:
        #     # Filter for Deliverys with dates less than or equal to the specified maximum
        #     conditions.append(Delivery.end_date <= date_max)

        # Filter the Deliverys based on the conditions
        print(conditions[0])
        ecomrequests = EcomRequest.query.filter(and_(*conditions)).all()
        print(ecomrequests)
    
    # print(op)

    return render_template('agentportal/claims.html',form=form,ecomrequests=ecomrequests,filterform=form)



@core.route("/addfarmer", methods=["GET", "POST"])
def addfarmer():
    form = FarmerForm()
    items  = Farmer.query.all()
    if request.method == "POST":
        # destination = Destination.query.filter_by(name=request.form["destination"]).first()
        # if not destination:
        #     return render_template("create_PartRequest.html", error="destination not found")
  
        farmer = Farmer( first_name=form.first_name.data,last_name=form.last_name.data, number=form.number.data,premium_amount=form.premium_amount.data,location=form.location.data)
        db.session.add(farmer)
        db.session.commit()
        return redirect(url_for("core.addfarmer"))
    return render_template("agentportal/addfarmer.html",form=form,items=items)

@core.route("/farmers", methods=["GET","POST"])
def farmers():
    form =  FilterForm()
    farmers = Farmer.query.all()
    print ("deliveries")
    print(farmers)
    if request.method == "POST":
        # Get the filter values from the form
        first_name = form.first_name.data
        print (first_name)
        last_name= form.last_name.data
        location = form.location.data
        number = form.number.data

        # Build the SQLAlchemy filter conditions
        conditions = []
        if first_name:
            conditions.append(Farmer.first_name == first_name)
        if last_name:
            conditions.append(Farmer.last_name == last_name)
        if number:
            # Build a list of conditions that match the location field
            # using the LIKE operator and the % wildcard
            number_conditions = [
                Farmer.number.like(f"%{number}%"),
                Farmer.number.like(f"{number}%"),
                Farmer.number.like(f"%{number}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*number_conditions))
        if location:
            # Build a list of conditions that match the destination field
            # using the LIKE operator and the % wildcard
            location_conditions = [
                Farmer.location.like(f"%{location}%"),
                Farmer.location.like(f"{location}%"),
                Farmer.location.like(f"%{location}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the destination variations
            conditions.append(or_(*location_conditions))
        # if status and status != "all":
        #     conditions.append(Delivery.delivery_status == status)
        # if date_min and date_max:
        #     # Filter for Deliverys with dates within the specified range
        #     conditions.append(and_(Delivery.start_date >= date_min, Delivery.end_date <= date_max))
        # elif date_min:
        #     # Filter for Deliverys with dates greater than or equal to the specified minimum
        #     conditions.append(Delivery.start_date >= date_min)
        # elif date_max:
        #     # Filter for Deliverys with dates less than or equal to the specified maximum
        #     conditions.append(Delivery.end_date <= date_max)

        # Filter the Deliverys based on the conditions
        print(conditions[0])
        farmers = Farmer.query.filter(and_(*conditions)).all()
    # user = User.query.filter_by(id=session['id']).first()

    return render_template("agentportal/farmers.html", farmers=farmers,form=form,filterform=form)


@core.route("/farmer/<int:id>", methods=["POST",'GET'])
def farmer(id):
    form = FarmerForm()
    farmer = Farmer.query.filter_by(id=id).first()
    farmers = Farmer.query.all()


    

    if request.method == "POST":
        farmer.first_name = form.first_name.data
        farmer.last_name = form.last_name.data
        farmer.number = form.number.data
        farmer.premium_amount = form.premium_amount.data
        farmer.location = form.location.data
        # bid.status = 'bid'
        
        db.session.commit()
        
    
        return redirect(url_for("core.farmers"))
    
    elif request.method == 'GET':
        form.first_name.data = farmer.first_name
        form.last_name.data = farmer.last_name
        form.number.data = farmer.number
        form.premium_amount.data = farmer.premium_amount
        form.location.data = farmer.location
      
        
    return render_template("agentportal/farmer.html",farmer=farmer, form=form)


@core.route('/uploadfarmer',methods=['GET', 'POST'])
def uploadfarmer():
    form = FarmerForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    
    data= []

    if request.method == 'POST':
        if form.uploadfile.data:

            uploaded_file = request.files['uploadfile'] 
            print("file")
            print(uploaded_file.filename)
            filepath = os.path.join(current_app.root_path, uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath, encoding='utf-8-sig') as file:
                csv_file = csv.reader(file)
                print(csv_file)
                line_count= 0
                for row in csv_file:
                    line_count += 1
                    print(line_count)
                    try:
                        farmers_save = Farmer(first_name=row[0],last_name=row[1],number=row[2],location=row[3],premium_amount=row[4])
                        db.session.add(farmers_save)
                        db.session.commit()
                    except Exception as e:
                        # Add the line number to the error message
                        error_message = f"Error on line {line_count}: {str(e)}"
                        # Handle the error appropriately
                        message = error_message
                    
                    print(row)
                    
                    
                    # data.append(row)
                    # farmers_save = Farmer(first_name=row[0],last_name=row[1],number=row[2],location=row[3],premium_amount=row[4])
                    # db.session.add(farmers_save)
                    # db.session.commit()
                    # print("data")
                    # print(data)
                return  redirect(url_for('core.farmers'))
        # else:
        #     farmers_save = Farmer(code=form.code.data,cost=form.cost.data,country=form.country.data,route=form.route.data)
        #     db.session.add(farmers_save)
        #     db.session.commit()
    return render_template('agentportal/uploadfarmer.html',form=form,user=user)


@core.route('/api/addfarmer',methods=['GET','POST'])
# @jwt_required()
def addplan():
    farmer = Farmer.query.all()

    first_name = request.json['first_name'] 
    last_name = request.json['last_name'] 
    premium_amount = request.json['premium_amount'] 
    location = request.json['location']
    number = request.json['number']

    plan = Farmer(first_name=first_name,
                            premium_amount=premium_amount,
                            last_name=last_name,number=number,location=location
                            )
    db.session.add(farmer)
    db.session.commit()
    status = 1
    if status == 1:
        return jsonify(first_name,last_name,premium_amount,"success")
    else:
        return jsonify("Failed")
  
  
  
@core.route('/api/checknumber',methods=['GET','POST'])
@require_api_key
def checknumber():
     
    # print(request.args.get('number'))

    # number = requests.json['number'] 
    number = request.args.get('number')
 
    farmer = Farmer.query.filter_by(number=number).first()
    if farmer is not None:
        
        ecomrequest =  EcomRequest(number=number,country=farmer.country,farmer_id=farmer.id,cashcode=farmer.cashcode)
        db.session.add(ecomrequest)
        db.session.commit()
        
        # endPoint = 'https://api.mnotify.com/api/sms/quick'
        # # apiKey = 
        message = "Hi " +farmer.first_name + " "+ farmer.last_name  +" , your 2022/2023 premium is GHS" + str(farmer.premium_amount) + " and be paid on " +number +". Your cash code is XXXX.  Reach out to ECOM on 0800189189 for more enquires."
        # print("message")
        # print(message)
        # data = {
        # 'recipient[]':number,
        # 'sender': 'Ecom',
        # 'message': message,
        # 'is_schedule': False,
        # 'schedule_date': " "
        # }
        # url = endPoint + '?key=' + akey
        # # if credit_balance > number_messages:
        # response = requests.post(url, data)
        # response_data = response.json()
        # print("response_data")
        # print(response_data)
        url = 'http://rslr.connectbind.com:8080/bulksms/bulksms'
        # apiKey = 
        rpassword = environ.get('ROUTESMS_PASS')
        data = {
            'username': 'dlp-testacc',
            'password': rpassword,
            'type':'0',
            'dlr':'1',
            'destination':number,
            'source':'test',
            'message':message
        }
        response = requests.post(url, data)

        # response_data = response.json()
        # print("response_data")
        res = response.text.split("|")
        print(res)

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
    
