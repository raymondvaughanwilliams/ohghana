from flask import render_template,request,Blueprint,session,redirect,url_for,jsonify
from structure.models import User,About,Price, WebFeature,Faq,Testimonial,Team,Appearance,Block,Journal ,Payment,NewsletterContacts,Delivery,Destination
# from structure.team.views import team
from structure.web_features.forms import WebFeatureForm
from structure.team.forms import UpdateTeamForm
from structure.userportal.forms import SessionForm
from structure.about.forms import UpdateAboutForm
from structure.faq.forms import FaqForm
from structure.pricing.forms import PriceForm
from structure.testimonial.forms import TestimonialForm
from structure.about.forms import AboutForm
from structure.block.forms import BlockForm
from structure.core.forms import BookingForm,UpdateSessionForm ,JournalForm,Addtherapist ,NewsletterForm,FilterForm
from structure.userportal.forms import ContactForm
from sqlalchemy.orm import load_only
from flask_login import login_required
from structure.appearance.forms import AppearanceForm
from structure.block.forms import BlockForm
from structure.users.forms import LoginForm
from structure.appearance.views import appearance
from structure.models import Appearance,Book
from flask_mail import Mail, Message
from structure import mail,db,app
from datetime import datetime,timedelta
import urllib.request, json
import random
from sqlalchemy import  and_, or_ ,desc ,asc 



web = Blueprint('web',__name__)



@web.route('/',methods=['GET', 'POST'])
def home():
    aboutform = AboutForm()
    newsletterform = NewsletterForm()

    page = request.args.get('page', 1, type=int)
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    # alltherapists = Therapist.query.all()
    therapists = WebFeature.query.order_by(WebFeature.date.desc()).all()
    about = About.query.get(1)
    price = Price.query.all()
    faq = Faq.query.all()
    testimonial = Testimonial.query.all()
    team= Team.query.all()
    serv = Price.features
    Blockform= BlockForm()
    team= Team.query.all()
    block= Block.query.all()
    Appearanceform = AppearanceForm()
    appearance=Appearance.query.all()
    # print(web_features.items)
    webfeatureform = WebFeatureForm()
    priceform = PriceForm()
    faqform = FaqForm()
    testimonialform = TestimonialForm()
    
    
    therapistobj = User.query.filter_by(role="therapist").all()
    
    if request.method == "POST":
        name = newsletterform.name.data
        phone = newsletterform.phone.data
        email = newsletterform.email.data
        contact = NewsletterContacts(name = name, phone = phone, email = email)
        db.session.add(contact)
        db.session.commit()
    # teammateform = Team()
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('web/homepage.html',testimonialform= testimonialform,faqform=faqform, therapists = therapists,web_features=web_features, about=about,pricing=price,faq=faq,testimonial=testimonial,team=team,serv=serv,Blockform=Blockform,appearance=appearance,Appearanceform=Appearanceform,block=block,aboutform=aboutform,webfeatureform= webfeatureform,priceform=priceform,therapistobj=therapistobj,newsletterform=newsletterform)



@web.route('/wtherapistdetails/<int:id>')
def viewtherapist(id):
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''

    page = request.args.get('page', 1, type=int)
    # web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    # therapist = WebFeature.query.get_or_404(id)
    therapists = User.query.all()
    print("therapist:")
    print(therapists)
    about = About.query.get(1)
    price = Price.query.all()
    faq = Faq.query.all()
    testimonial = Testimonial.query.all()
    team= Team.query.all()
    serv = Price.features
    Blockform= BlockForm()
    team= Team.query.all()
    block= Block.query.all()
    Appearanceform = AppearanceForm()
    appearance=Appearance.query.all()
    therapistobj= User.query.filter_by(id=id).first()
    print(therapistobj)
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('web/viewtherapist.html',about=about,pricing=price,faq=faq,testimonial=testimonial,team=team,serv=serv,Blockform=Blockform,appearance=appearance,Appearanceform=Appearanceform,block=block,therapistobj=therapistobj)





@web.route("/pricelist/<int:id>", methods=['GET', 'POST'])
@login_required
def pricelist(id):

    pricing = Price.query.all()
    tid = id
    # if pricing:
    #     title = pricing.title
    #     amount = pricing.amount
    #     features = pricing.features
    #     services=[]
    #     service= pricing.features.split(',')
    #     services.append(service)
    return render_template('web/pricelist.html',pricing=pricing,tid=tid)





@web.route("/buypackage/<int:id>/<int:tid>")
@login_required
def buypackage(id,tid):
    price = Price.query.get_or_404(id)
    userdemail = session['email']
    user =  User.query.filter_by(email=userdemail).first()
    name = user.name
    number = user.number
    # random_num = randint(1,1000)
    tx_ref = user.email[0:6]+ str(random.randint(1,1000))
    tid = tid
    return render_template('web/orderdetails.html',price=price,useremail=userdemail,tx_reff=tx_ref,name=name,number=number,tid=tid,user=user)




@web.route("/confirmpayment")
@login_required
def confirmpayment():
    user = User.query.filter_by(email=session['email']).first()
    uid = user.id
    
    if request.args.get('status') == "successful":
        transaction_id = request.args.get('transaction_id')
        # user = User.query.filter_by(email=session['email']).first()
        status = request.args.get('status')
        tx_ref = request.args.get('tx_ref')
        amount = request.args.get('amount')
        tid = request.args.get('tid')
        sessions = request.args.get('sessions')
        
        print('sessions')
        print(sessions)
        amount_dict = amount.split(' ')
        price = amount_dict[0]
        plan = Price.query.filter_by(amount=amount).first()

        user.rec_transaction_id = transaction_id
        user.therapist_id = tid
        user.rem_sessions = user.rem_sessions+ int(sessions)





        print(amount_dict)
        print(amount)
        payment = Payment(transaction_id=transaction_id,
                             tx_ref=tx_ref,
                             user_id =uid,status=status,amount=price,plan_id = "ttt"
                             )
        db.session.add(payment)
        db.session.commit()
        

        return redirect(url_for('userportal.userdash'))





@web.route("/paymentconfirmation/<int:plan_id>")
@login_required
def paymentconfirmation(plan_id):
    plan = Price.query.filter_by(id = plan_id).first()

    return render_template('web/paymentconfirmation.html',plan=plan)





@web.route("/booktherapist/<int:tid>",methods=['GET', 'POST'])
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
    return render_template('web/bookingdetails.html',total=total,tx_reff=tx_ref,tid=tid,user=user,therapist=therapist,form=form,sessions=sessions)



@web.route('/therapists')
def alltherapists():
    therapists = User.query.filter_by(role="therapist").all()
    return render_template('web/therapists.html',therapists=therapists)
    
    
@web.route('/how-it-works')
def howitworks():
    return render_template('web/howitworks.html')


@web.route('/our-services')
def ourservices():
    return render_template('web/services.html')





@web.route('/faq')
def faqs():
    return render_template('web/faqs.html')


@web.route('/contact-us',methods=['GET', 'POST'])
def contact_us():
    form = ContactForm()
    if request.method == 'POST':
        print("ajk")
        print(form.hidden.data)
        print(form.name.data)
        
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
        return redirect(url_for('web.home'))

            
    return render_template('web/contactus.html',form=form)











@web.route('/home',methods=['GET', 'POST'])
def web_home():
    aboutform = AboutForm()
    newsletterform = NewsletterForm()
    filterform = FilterForm()
    destinations = Destination.query.all()
    page = request.args.get('page', 1, type=int)
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    # alltherapists = Therapist.query.all()
    therapists = WebFeature.query.order_by(WebFeature.date.desc()).all()
    about = About.query.get(1)
    price = Price.query.all()
    faq = Faq.query.all()
    testimonial = Testimonial.query.all()
    team= Team.query.all()
    serv = Price.features
    Blockform= BlockForm()
    team= Team.query.all()
    block= Block.query.all()
    Appearanceform = AppearanceForm()
    appearance=Appearance.query.all()
    # print(web_features.items)
    webfeatureform = WebFeatureForm()
    priceform = PriceForm()
    faqform = FaqForm()
    testimonialform = TestimonialForm()
    deliveries = Delivery.query.filter_by(delivery_status="pending").all()
    
    
    therapistobj = User.query.filter_by(role="therapist").all()
    
    if request.method == "POST":
        name = newsletterform.name.data
        phone = newsletterform.phone.data
        email = newsletterform.email.data
        contact = NewsletterContacts(name = name, phone = phone, email = email)
        db.session.add(contact)
        db.session.commit()
    # teammateform = Team()
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('website/index.html',deliveries =deliveries, about=about,pricing=price,faq=faq,Blockform=Blockform,block=block,aboutform=aboutform,newsletterform=newsletterform,testimonials=testimonial,destinations=destinations,filterform=filterform)


@web.route('/packages',methods=['GET', 'POST'])
def packages():
    filterform = FilterForm()
    packages = Delivery.query.filter_by(delivery_status="pending")
    destinations = Destination.query.all()
    user =User.query.filter_by(id=session['id'])
    if request.method == "POST":
        # Get the filter values from the form
        location = filterform.location.data
        destination = filterform.destination.data
        date_min = filterform.start_date.data
        date_max = filterform.end_date.data
        # Build the SQLAlchemy filter conditions
        conditions = []
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
        if date_min and date_max:
            # Filter for Deliverys with dates within the specified range
            print(Delivery.start_date)
            print(date_min)
            conditions.append(and_(Delivery.start_date >= date_min, Delivery.end_date <= date_max))
        conditions.append(Delivery.delivery_status == "pending")
        print(conditions[0])
        # elif date_min:
        #     # Filter for Deliverys with dates greater than or equal to the specified minimum
        #     conditions.append(Delivery.start_date >= date_min)
        # elif date_max:
        #     # Filter for Deliverys with dates less than or equal to the specified maximum
        #     conditions.append(Delivery.end_date <= date_max)

        # Filter the Deliverys based on the conditions
        packages = Delivery.query.filter(and_(*conditions)).all()
        print(packages)
        print('packages')
        return render_template("website/packages.html", packages=packages,user=user,filterform=filterform,destinations=destinations)

    return render_template('website/packages.html',packages=packages,filterform=filterform,destinations=destinations)