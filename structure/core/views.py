from flask import render_template,request,Blueprint,session,redirect,url_for,jsonify
from structure.models import User,About,Faq,Testimonial,PartRequest,Bid,Review
# from structure.team.views import team

from structure.about.forms import AboutForm
from structure.core.forms import DeliveryForm,RequestForm,BidForm,AcceptBidForm,ReviewForm
from sqlalchemy.orm import load_only
from flask_login import login_required
from flask_mail import Mail, Message
from structure import mail,db,photos
from datetime import datetime,timedelta
import urllib.request, json
import secrets



core = Blueprint('core',__name__)


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