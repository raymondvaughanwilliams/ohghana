import atexit
import csv
import os
from os import environ
from uuid import uuid4
import secrets
import string
import requests
from requests.auth import HTTPBasicAuth
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, Blueprint, session, redirect, url_for, jsonify, current_app, request
from flask_login import login_required
from sqlalchemy import and_, or_, desc
from flask_mail import Mail, Message

from structure import db,mail 
from structure.core.forms import FilterForm, FarmerForm ,ResultForm,CheckResultForm,StudentForm,SipRequestForm
from structure.models import User, About, Farmer, EcomRequest , StudentResult , Subject ,SipRequest

core = Blueprint('core', __name__)

API_KEY = os.environ.get('API_KEY')
connex_username = os.environ.get('connex_username')
connex_password = os.environ.get('connex_password')


def require_api_key(view_function):
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid API key', 'status': False}), 401

    return decorated_function

def generate_secure_password(length=12):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    secure_password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return secure_password

@core.route('/base')
def base():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    about = About.query.all()
    return render_template('base.html', about=about)





@core.route('/agent/dashboard')
@login_required
def agent_dashboard():
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)
    name = "ecom"
    session.pop('msg', None)

    subjects = Subject.query.order_by(desc(Subject.id)).all()
    studentresults = StudentResult.query.order_by(desc(StudentResult.id)).all()
    farmers = Farmer.query.order_by(desc(Farmer.id)).all()
    ecom_requests = EcomRequest.query.order_by(desc(EcomRequest.id)).all()

    form = FilterForm()
    if session['role'] == 'agent':
        name = user.name

    return render_template(
        'agentportal/dashboard.html',
        form=form, user=user, about=about,
        name=name, farmers=farmers, ecomrequests=ecom_requests,
        subjects=subjects,studentresults=studentresults
    )




@core.route("/delete_result/<int:result_id>", methods=['POST', 'GET'])
@login_required
def delete_result(result_id):
    result = StudentResult.query.get_or_404(result_id)
    db.session.delete(result)
    db.session.commit()
    return redirect(url_for('core.results'))


@core.route("/api/delete_farmers", methods=['POST', 'GET'])
def delete_farmers():
    farmers = request.args.get('farmers')
    farmers_list = [int(farmer) for farmer in farmers.split(",")]
    successfully_deleted = []
    failed = []

    for thefarmer in farmers_list:
        farmer = Farmer.query.filter_by(id=thefarmer).first()
        if farmer:
            db.session.delete(farmer)
            db.session.commit()
            successfully_deleted.append(thefarmer)
        else:
            failed.append(thefarmer)

    payload = {
        "status": True,
        "message": " Farmers deleted",
        "successful": successfully_deleted,
        "failed": failed
    }

    return jsonify(payload), 200




@core.route("/studentsapi", methods=["GET", "POST"])
def studentsapi():
    students = User.query.filter_by(role='student').all()
    student_list = []

    if students:
        for student in students:
            payload = {
                "id": student.id,
                "name": student.name,
                "index_number": student.index_number,
                "completed_year": student.completed_year,
             
            }
            student_list.append(payload)

        context = {
            "status": True,
            "message": " student found!",
            "data": student_list,
        }

        return jsonify(context), 200
    else:
        context = {
            "status": False,
            "message": "student not found",
            "error": "null"
        }

        return jsonify(context), 404

@core.route("/resultsapi", methods=["GET", "POST"])
def resultsapi():
    results = StudentResult.query.all()
    results_list = []
    print("resultsapi")

    if results:
        for result in results:
            payload = {
                "id": result.id,
                "name": result.student.name,
                "subject": result.subject.name,
                "result": result.result,
                "completed_year": result.student.completed_year,
                "index_number": result.index_number
                
            }
            results_list.append(payload)

        context = {
            "status": True,
            "message": " result found!",
            "data": results_list,
        }

        return jsonify(context), 200
    else:
        context = {
            "status": False,
            "message": "result not found",
            "error": "null"
        }

        return jsonify(context), 404

@core.route("/studentapi/<int:id>", methods=["GET", "POST"])
def studentapi(id):
    user = User.query.filter_by(id=id).first()
    results = StudentResult.query.filter_by(index_number=user.index_number).all()
    results_list = []
    print("studenting")
    print(user)
    print(results)

    if results:
        for result in results:
            payload = {
                "id": result.id,
                "name": user.name,
                "subject": result.subject.name,
                "result": result.result,
                "completed_year": result.student.completed_year,
                "index_number": result.index_number
                
            }
            results_list.append(payload)

        context = {
            "status": True,
            "message": " result found!",
            "data": results_list,
        }

        return jsonify(context), 200
    else:
        context = {
            "status": False,
            "message": "result not found",
            "error": "null"
        }

        return jsonify(context), 404


# @core.route("/report", methods=["GET"])
# @login_required
# def report():
#     return render_template("agentportal/report.html")



@core.route('/', methods=['GET', 'POST'])
# @require_api_key
def siprequests():
    form = SipRequestForm()
    user = User.query.filter_by(id=session['id']).first()
    if request.method =="POST":
        siprequest = SipRequest(
            channels=form.channels.data,
            other=form.other.data,
            codecs=form.codecs.data,
            certificate = form.certificate.data,
            inbound = form.inbound.data,
            outbound = form.outbound.data,
            provider = form.provider.data     
        )
        db.session.add(siprequest)
        db.session.commit()      
        connex_username = 'raymond@delaphonegh.com'
        connex_password = 'Passw0rd@100'
        # Create a new customer using Connex CS API
        customer_data = {
            "name": user.username,  # You can modify this as per your requirement
            "portal_access": "yes",
            "channels": siprequest.channels,
            "portal_username": user.email,
            "portal_password":user.email  

                
                    # You can modify this as per your requirement
            # Include other customer data fields as needed
        }
        headers = {
            
            "Content-Type": "application/json"
        }
        # create_customer_response = requests.post(
        #     "https://app.connexcs.com/api/cp/customer",
        #     json=customer_data,
        #     headers=headers
        # )
        create_customer_response = requests.post(
            "https://app.connexcs.com/api/cp/customer",
            json=customer_data,
            headers=headers,
            auth=HTTPBasicAuth(connex_username, connex_password)
        )
        create_customer_response_data = create_customer_response.json()
        print(create_customer_response_data)
        
        # Create a SIP user for the new customer using Connex CS API
        sip_user_data = {
            "username": user.username,  # You can modify this as per your requirement
            "customer_id": create_customer_response_data["id"],
            # Include other SIP user data fields as needed
        }
        create_sip_user_response = requests.post(
            "https://app.connexcs.com/api/cp/switch/user",
            json=sip_user_data,
            headers=headers,
            auth=HTTPBasicAuth(connex_username, connex_password)
        )
        print(create_sip_user_response)
     
        return render_template("viewresult.html",user=user)



    return render_template("index.html",form=form)




@core.route('/newsiprequestapi', methods=['POST'])
def newsiprequest():
    print("request")
    print(request)
    password = generate_secure_password()
 
    if request.method == 'POST':
        print(request)
        print(request.args)
        print(request.form)
        print("name")
        print(request.args.get('name'))
        print(request.form.get('name'))
        
        
        customer_data = {
            "name": request.args.get('name'),
            "portal_access": "yes",
            "channels": request.args.get('channels'),
            "portal_username": request.args.get('email'),
            "portal_password": password,
            "portal_url": "portal.delaphonegh.com" ,
            "portal_access":"yes",
            "is_customer":"yes",
            "currency":"GHS"

            # Include other customer data fields as needed
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        
        create_customer_response = requests.post(
            "https://app.connexcs.com/api/cp/customer",
            json=customer_data,
            headers=headers,
            auth=HTTPBasicAuth(connex_username, connex_password)
        )
        
        create_customer_response_data = create_customer_response.json()
        print("create_customer_response_data")
        print(create_customer_response_data)
        
        contact_data = {
            "email": request.args.get('email'),
              "password":customer_data['portal_password'],
            "customer_id": create_customer_response_data["id"],
            # Include other SIP user data fields as needed
        }
        
        create_contact = requests.post(
            "https://app.connexcs.com/api/cp/contact",
            json=contact_data,
            headers=headers,
            auth=HTTPBasicAuth(connex_username, connex_password)
        )
        print("contact info")
        print(create_contact)
        sip_request = SipRequest(
            channels = request.args.get('channels'),
            other = request.args.get('channels'),
            codecs = request.args.get('codecs'),
            certificate = request.args.get('certificate'),
            inbound = request.args.get('inbound'),
            outbound = request.args.get('outbound'),
            provider = request.args.get('provider'),
            name = request.args.get('name'),
            email = request.args.get('email'),
            customer_id = create_customer_response_data["id"]

        )
        
        db.session.add(sip_request)
        db.session.commit()
        msg = Message(
        sender = "info@delaphonegh.com",
        subject="Delaphone Portal Information",
        recipients=[sip_request.email],
        # recipients=['raymondvaughanwilliams@gmail.com'],
        # html="<p>Package has been created.<p>Details:<br><ul><li>Item:{}</li><li>Sender Location:{}</li><li>Destination:{}</li><li>Price:{}</li><li>Start Date:{}</li><li>End Date:{}</li></ul>".format( form.item_description.data,  delivery.sender_location.name,delivery.sender_location.name,delivery.price,form.start_date.data,form.end_date.data)
        html= render_template('mails/welcome.html', sip_request=sip_request,password=password)

        )
        mail.send(msg)
        print("sent welcome message")
        msg = Message(
        sender = "info@delaphonegh.com",
        subject="New Client ",
        recipients=['raymond@delaphonegh.com'],
        # recipients=['raymondvaughanwilliams@gmail.com'],
        # html="<p>Package has been created.<p>Details:<br><ul><li>Item:{}</li><li>Sender Location:{}</li><li>Destination:{}</li><li>Price:{}</li><li>Start Date:{}</li><li>End Date:{}</li></ul>".format( form.item_description.data,  delivery.sender_location.name,delivery.sender_location.name,delivery.price,form.start_date.data,form.end_date.data)
        html= render_template('mails/newcustomer.html', sip_request=sip_request)

        )
        mail.send(msg)
        
        return jsonify({"message": "Success"})
    
    return "Welcome to the SIP Request API"


@core.route("/siprequestsapi", methods=["GET", "POST"])
def siprequestsapi():
    siprequests = SipRequest.query.all()
    siprequest_list = []

    if siprequests:
        for siprequest in siprequests:
            payload = {
                "id": siprequest.id,
                "channels": siprequest.channels,
                "inbound": siprequest.inbound,
                "outbound": siprequest.outbound,
                "codecs": siprequest.codecs,
                "provider": siprequest.provider,
                "other":siprequest.other
             
            }
            siprequest_list.append(payload)

        context = {
            "status": True,
            "message": " siprequest found!",
            "data": siprequest_list,
        }

        return jsonify(context), 200
    else:
        context = {
            "status": False,
            "message": "siprequest not found",
            "error": "null"
        }

        return jsonify(context), 404




@core.route("/siprequestapi/<int:id>", methods=["GET", "POST"])
def siprequestapi(id):
    user = User.query.filter_by(id=id).first()
    results= SipRequest.query.filter_by(id=id).all()
    results_list = []
    print("siprequesting")
    print(user)
    print(results)

    if results:
        for result in results:
            payload = {
                "id": result.id,
                "channel": result.channel,
                "codecs": result.codecs.name,
                "inbound": result.inbound,
                "outbound": result.outbound,
                "provider":result.provider
                
            }
            results_list.append(payload)

        context = {
            "status": True,
            "message": " result found!",
            "data": results_list,
        }

        return jsonify(context), 200
    else:
        context = {
            "status": False,
            "message": "result not found",
            "error": "null"
        }

        return jsonify(context), 404



# scheduler = BackgroundScheduler()
# scheduler.add_job(func=resend_sms, trigger="interval", seconds=600)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())
