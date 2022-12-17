from flask import render_template,request,Blueprint,session,redirect,url_for,jsonify
from structure.models import User,About,Price, WebFeature,Faq,Testimonial,Team,Appearance,Block,Journal
# from structure.team.views import team
from structure.web_features.forms import WebFeatureForm
from structure.team.forms import UpdateTeamForm
from structure.about.forms import UpdateAboutForm
from structure.faq.forms import FaqForm
from structure.pricing.forms import PriceForm
from structure.testimonial.forms import TestimonialForm
from structure.about.forms import AboutForm
from structure.block.forms import BlockForm
from structure.core.forms import BookingForm,UpdateSessionForm ,JournalForm,Addtherapist
from sqlalchemy.orm import load_only
from flask_login import login_required
from structure.appearance.forms import AppearanceForm
from structure.block.forms import BlockForm
from structure.users.forms import LoginForm
from structure.appearance.views import appearance
from structure.models import Appearance,Book
from flask_mail import Mail, Message
from structure import mail,db
from datetime import datetime,timedelta
import urllib.request, json


core = Blueprint('core',__name__)

@core.route('/')
@login_required
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    about = About.query.get(1)
    faq = Faq.query.all()
    team = Team.query.all()
    pricing = Price.query.all()
    testimonial = Testimonial.query.all()
    feature_count = WebFeature.query.count()
    faq_count = Faq.query.count()
    team_count = Team.query.count()
    pricing_count = Price.query.count()
    testimonial_count = Testimonial.query.count()
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    return render_template('index.html',web_features=web_features,about=about,faq=faq,team=team,pricing=pricing,testimonial=testimonial,feature_count=feature_count,faq_count=faq_count,team_count=team_count,pricing_count=pricing_count,testimonial_count=testimonial_count)

@core.route('/base')
def base():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    about = About.query.all()
    return render_template('base.html',about=about)


@core.route('/hmsui')
def hmsui():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    aboutform = AboutForm()

    page = request.args.get('page', 1, type=int)
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    alltherapists = Therapist.query.all()
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
    print(web_features.items)
    webfeatureform = WebFeatureForm()
    priceform = PriceForm()
    faqform = FaqForm()
    testimonialform = TestimonialForm()
    # teammateform = Team()
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('web/homepage.html',testimonialform= testimonialform,faqform=faqform, therapists = therapists,web_features=web_features, about=about,pricing=price,faq=faq,testimonial=testimonial,team=team,serv=serv,Blockform=Blockform,appearance=appearance,Appearanceform=Appearanceform,block=block,aboutform=aboutform,webfeatureform= webfeatureform,priceform=priceform)

@core.route('/therapist/<int:id>')
def viewtherapist(id):
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''

    page = request.args.get('page', 1, type=int)
    # web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    therapist = WebFeature.query.get_or_404(id)
    print("therapist:")
    print(therapist)
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
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('web/viewtherapist.html',web_features=therapist, about=about,pricing=price,faq=faq,testimonial=testimonial,team=team,serv=serv,Blockform=Blockform,appearance=appearance,Appearanceform=Appearanceform,block=block)


@core.route('/addwebfeatureapi', methods=['POST'])
def addwebfeatureapi():
    print("api request")
    form = Addtherapist()
    # genre = Genre.query.all()
    # form.genre.choices = [(g.id, g.name) for g in Genre.query.filter_by(id='1').all()]
    date = request.json['date']
    title = request.json['title']
    wtext = request.json['wtext'] 
    price = request.json['price']
    type = request.json['type']
    email = request.json['email']
    city = request.json['city']
    phone = request.json['phone'] 

    webfeature = WebFeature(title= title,price=price,date=date,wtext=wtext,type=type,email=email,city=city,phone=phone)
    db.session.add(webfeature)
    db.session.commit()
    return WebFeatureSchema.jsonify(webfeature)


@core.route('/alltherapists', methods=['GET'])
def therapists():
    web_features = WebFeature.query.all()
    results = WebFeatureSchema(many=True)
    output = results.dump(web_features)
    return jsonify(output)



@core.route('/book/<int:id>',methods=['GET','POST'])
@login_required
def book(id):
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''

    page = request.args.get('page', 1, type=int)
    # web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    therapist = WebFeature.query.get_or_404(id)
    print("email:")
    print(therapist)
    
    ses_email = session['email']
    print(ses_email)
    userdetails = User.query.filter_by(email=ses_email).first()
    print("userdetails:")
    print(userdetails)
    locate = userdetails.location
    mobile = userdetails.number
    uid = userdetails.id
    dbid = Book.query.order_by(Book.id.desc()).first()
    nid = dbid.id + 1
    print("uid:")
    print(nid)


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
    form = BookingForm()
    # services=[]
    # service= serv.split(',')
    # services.append(service)

    if request.method == 'POST':
        email = session['email']
        phone = mobile
        name = session['name']
        message = form.message.data
        date = form.date.data
        location = locate
        time = form.time.data

        subject = "blot mail"
        booking = Book(name=name,
                             email=email,
                             date=date,phone=phone,location=location,
                             therapist_id = id, time=time,user_id=uid,message=message
                             )
        db.session.add(booking)
        db.session.commit()
        print("Booking Created")  
        return redirect(url_for('core.hmsui') )    

        # msg = Message(subject,sender = email,recipients = ["raymond@delaphonegh.com"])
        # msg.body = "name: " + name + "\n" + "\n" + "mobile: " + phone  + "\n" + "message: " + message
        # mail.send(msg)
        # return redirect(url_for('core.thankyou'))
    # return render_template('temp.html',form=form,messageform=messageform)
    return render_template('book.html',web_features=therapist, about=about,pricing=price,faq=faq,testimonial=testimonial,team=team,serv=serv,Blockform=Blockform,appearance=appearance,Appearanceform=Appearanceform,block=block,form=form)




@core.route('/booknow/<int:id>',methods=['GET','POST'])
@login_required
def booknow(id):
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''

    # web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    therapist = WebFeature.query.get_or_404(id)
    print("email:")
    print(therapist)
    
    ses_email = session['email']
    print(ses_email)
    userdetails = User.query.filter_by(email=ses_email).first()
    print("userdetails:")
    print(userdetails)
    locate = userdetails.location
    mobile = userdetails.number
    uid = userdetails.id
    dbid = Book.query.order_by(Book.id.desc()).first()
    nid = dbid.id + 1
    print("uid:")
    print(nid)


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
    form = BookingForm()
    # services=[]
    # service= serv.split(',')
    # services.append(service)

    if request.method == 'POST':
        email = session['email']
        phone = mobile
        name = session['name']
        message = form.message.data
        date = form.date.data
        location = locate
        time = form.time.data

        subject = "blot mail"
        booking = Book(name=name,
                             email=email,
                             date=date,phone=phone,location=location,
                             therapist_id = id, time=time,user_id=uid,message=message
                             )
        db.session.add(booking)
        db.session.commit()
        print("Booking Created")  
        return redirect(url_for('core.hmsui') )    

        # msg = Message(subject,sender = email,recipients = ["raymond@delaphonegh.com"])
        # msg.body = "name: " + name + "\n" + "\n" + "mobile: " + phone  + "\n" + "message: " + message
        # mail.send(msg)
        # return redirect(url_for('core.thankyou'))
    # return render_template('temp.html',form=form,messageform=messageform)
    return render_template('pricing-page.html',web_features=therapist, about=about,pricing=price,faq=faq,testimonial=testimonial,team=team,serv=serv,Blockform=Blockform,appearance=appearance,Appearanceform=Appearanceform,block=block,form=form)



@core.route('/editui')
@login_required
def editui():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    Webfeatureform= WebFeatureForm()
    Teammateform = UpdateTeamForm()
    Faqform = FaqForm() 
    Testimonialform = TestimonialForm()
    Pricingform = PriceForm()
    Aboutform = AboutForm()
    page = request.args.get('page', 1, type=int)
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    about = About.query.get(1)
    price = Price.query.all()
    faq = Faq.query.all()
    Blockform= BlockForm()
    testimonial = Testimonial.query.all()
    team= Team.query.all()
    block= Block.query.all()
    Appearanceform = AppearanceForm()
    appearance=Appearance.query.all()
    appearancef=Appearance.query.filter_by(id=1).first()
    if request.method == 'GET':
        Appearanceform.title_color.data = appearancef.title_color
        Appearanceform.subtitle_color.data = appearancef.subtitle_color
        Appearanceform.paragraph_color.data = appearancef.paragraph_color
        Appearanceform.title_font.data = appearancef.title_font
        Appearanceform.subtitle_font.data = appearancef.subtitle_font
        Appearanceform.paragraph_font.data = appearancef.paragraph_font
        Appearanceform.title_size.data = appearancef.title_size
        Appearanceform.subtitle_size.data = appearancef.subtitle_size
        Appearanceform.paragraph_size.data = appearancef.paragraph_size
        Appearanceform.bootstrap_class1.data = appearancef.bootstrap_class1
        Appearanceform.bootstrap_class2.data = appearancef.bootstrap_class2
        Appearanceform.bootstrap_class3.data = appearancef.bootstrap_class3

    # for appearances in appearance:
    #         appearance=Appearance.query.all()
    #         Appearanceform = AppearanceForm()
    #         Appearanceform.title_color.data = appearances.title_color
    #         Appearanceform.subtitle_color.data = appearances.subtitle_color
    #         Appearanceform.paragraph_color.data = appearances.paragraph_color
    #         Appearanceform.title_font.data = appearances.title_font
    #         Appearanceform.subtitle_font.data = appearances.subtitle_font
    #         Appearanceform.paragraph_font.data = appearances.paragraph_font
    #         Appearanceform.title_size.data = appearances.title_size
    #         Appearanceform.subtitle_size.data = appearances.subtitle_size
    #         Appearanceform.paragraph_size.data = appearances.paragraph_size
    #         Appearanceform.bootstrap_class1.data = appearances.bootstrap_class1
    #         Appearanceform.bootstrap_class2.data = appearances.bootstrap_class2
    #         Appearanceform.bootstrap_class3.data = appearances.bootstrap_class3


    # fields = ['id']
    # data = Testimonial.options(load_only(*fields)).all()
    emplist = []
    for faqs in faq:
        emplist.append("row:" +str(faqs.id))
    print(emplist)


    templist = []
    for testimonials in testimonial:
        templist= "row:" +str(testimonials.id)
    #     templist.append("row:" +str(testimonials.id))
    # print(templist)



    print(faq)
    context={
        'about':about,
        'web_features':web_features,
        'price':price,
        'faq':faq,
        'testimonial':testimonial,
        'team':team,
    }

    serv = Price.features
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('editui.html',block = block,web_features=web_features,appearancef =appearancef,about=about,webfeatureform = Webfeatureform,teammateform=Teammateform,faqform = Faqform,testimonialform=Testimonialform,priceform=Pricingform,aboutform=Aboutform,team=team,pricing=price,faq=faq,testimonial=testimonial,templist=templist,emplist=emplist,blockform=Blockform,appearanceform=Appearanceform,appearance=appearance)
    # return render_template('info.html',context=context,faq=faq)


@core.route('/user/dashboard')
def userdashboard():
    # user = User.query.filter_by(email=session["email"]).first()
    # if session["email"]:
    #     print("ya")
    # else:
    #     print("h")


    if session['role'] == 'user':


        user = User.query.filter_by(email=session["email"]).first()

        about = About.query.get(1)
        op = user.plan_id
        bookings = Book.query.filter_by(email=session["email"]).all()
        todaysdate = datetime.now() 
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
                # print(previoussessions)



        # upcomingbookings = Book.query.filter_by(date >= todaysdate).all()
        # upcomingbookings = Book.query.order_by(Book.date.desc())
        # print("upcoming:")
        # print(upcomingsessions)

        sesh = Book.query.get(8)

        name = user.name
        # print(op)

        # print(comment.user.title)
        therapist_ids = []
        therapistss = {}
        for booking in bookings:
            # therapistss.append(booking.webfeatures.title)
            therapistss[booking.id] = booking.webfeatures.title
            # print(booking.webfeatures.id)
        # print(therapistss)
        # for key in therapistss:
        #     print(key)
        
        
        # print(therapistss)
        plan = Price.query.filter_by(id=op).first()
        print(plan)
        if user.rem_sessions > 0:
            rem_sessions = user.rem_sessions
            rem_chatweeks = user.rem_chatweeks
        return render_template('dashboarduser.html',about=about,plan=plan,rem_sessions=rem_sessions,rem_chatweeks=rem_chatweeks,bookings=bookings,therapistss=therapistss,name=name,upcoming=upcomingsessions,previoussessions=previoussessions)
    
    else:
        return render_template('error_pages/403.html')




@core.route('/therapysession/<int:id>')
def viewtherapysession(id):
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''

    # web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    # print("therapist:")
    # print(therapist)
   
    updateform = UpdateSessionForm()

    # therapysession = Book.query.get(id)
    therapysession = Book.query.get(id)
    about = About.query.get(1)

    alth = Book.query.all()
    team= User.query.all()

    print(therapysession)
    print("hm")
    print(alth)
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('viewsession.html',session=therapysession,updateform=updateform,about=about)



@core.route('/updatesession/<int:id>', methods=['GET', 'POST'])
def update_session(id):
    therapysession = Book.query.filter_by(id=id).first()
    form = UpdateSessionForm()

            # user = User.query.filter_by(email=form.email.data).first()
    if request.method == 'POST':

        
        therapysession.date = form.date.data
        therapysession.time = form.time.data
   
    print(therapysession.date)
    # book.time = 

    db.session.commit()
    return redirect(url_for('core.userdashboard'))


@core.route('/sidebar')
def sidebar():
    return render_template('sidebar.html')


@core.route('/journal')
def journal():
    user = User.query.filter_by(email=session['email']).first()
    uid = user.id
    journals = Journal.query.filter_by(user_id =uid)

  
    return render_template('journal.html',journals=journals)

@core.route('/journal/add',methods=['GET','POST'])
def journal_add():
    form = JournalForm()
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
        return redirect(url_for('core.journal'))    

    return render_template('addjournal.html',form=form)


@core.route('/journal/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def journal_edit(id):
    # user = User.query.filter_by(email=session['email']).first()
    # uid = user.id
    journal = Journal.query.filter_by(id =id).first()
    text= journal.text
    form = JournalForm()

            # user = User.query.filter_by(email=form.email.data).first()
    if request.method == 'POST':

        
        journal.text = form.text.data
   
    # book.time = 

        db.session.commit()
        return redirect(url_for('core.journal'))

  
    return render_template('editjournal.html',journal=journal,form=form,text=text)


@core.route("/<int:id>/delete_faq", methods=['POST','GET'])
@login_required
def delete_journal(id):
    journal = Journal.query.get_or_404(id)
    db.session.delete(journal)
    db.session.commit()
    return redirect(url_for('core.journal'))



@core.route("/user/therapysessions")
@login_required
def therapysessions():
    bookings = Book.query.filter_by(email=session["email"]).all()
    todaysdate = datetime.now() 
    print("todaysdate")
    print(todaysdate)
    upcomingsessions ={}
    previoussessions = {}
    for booking in bookings:
        if booking.date > todaysdate:
            # upcomingsessions.append(booking.webfeatures.title)
            upcomingsessions[booking.id] = booking.webfeatures.title
            print(upcomingsessions)
        else:
            previoussessions[booking.id] = booking.webfeatures.title
            print(previoussessions)
    return render_template('sessions.html',upcomingsessions=upcomingsessions,previoussessions=previoussessions)



@core.route('/locologin')
def locologin():
    therapists = WebFeature.query.order_by(WebFeature.date.desc()).all()
    form = LoginForm()
    return render_template('mainbase.html',therapists=therapists,form=form)




@core.route('/services')
def services():
    return render_template('services.html')


@core.route('/contact')
def contact():
    return render_template('contact.html')


@core.route('/howitworks')
def howitworks():
    return render_template('how-it-works.html')


@core.route('/faqs')
def faqs():
    return render_template('f-a-qs.html')