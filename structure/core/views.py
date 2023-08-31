import atexit
import csv
import os
from os import environ
from uuid import uuid4
import secrets
import random
import string
import requests
from requests.auth import HTTPBasicAuth
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template, Blueprint, session, redirect, url_for, jsonify, current_app, request
from flask_login import login_required
from sqlalchemy import and_, or_, desc
from flask_mail import Mail, Message

from structure import db,mail ,photos
from structure.core.forms import FilterForm,SipRequestForm
from structure.models import User, About, SipRequest, CDR , Contact

core = Blueprint('core', __name__)

API_KEY = os.environ.get('API_KEY')
connex_username = os.environ.get('connex_username')
connex_password = os.environ.get('connex_password')
APP_ID = os.environ.get('APP_ID')
APP_KEY = os.environ.get('APP_KEY')

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




allowed_extensions = ['png', 'jpg', 'jpeg', 'gif','txt']
def check_file_extension(filename):
    return filename.rsplit('.', 1)[1].lower() in allowed_extensions


@core.route('/base')
def base():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    about = About.query.all()
    return render_template('base.html', about=about)


@core.route('/things')
def things():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''
    about = SipRequest.query.all()
    return render_template('things.html', about=about)



@core.route('/agent/dashboard')
@login_required
def agent_dashboard():
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)
    name = "ecom"
    headers = {
        'Content-Type': 'application/json'
    }
    session.pop('msg', None)
    api_url = 'https://app.connexcs.com/api/cp/customer?status=inactive'
    # response = requests.get(api_url)
    response = requests.get(api_url, headers=headers,auth=HTTPBasicAuth(connex_username, connex_password))
    inactive = response.json() if response.status_code == 200 else []
    # print(response.content)
    lowbalance_url = 'https://app.connexcs.com/api/cp/customer'
    # lowbalance_response = requests.get(lowbalance_url)
    lowbalance_response = requests.get(lowbalance_url, headers=headers,auth=HTTPBasicAuth(connex_username, connex_password))
    lowbalance_response = lowbalance_response.json() if lowbalance_response.status_code == 200 else []
    low_balance = [entry for entry in lowbalance_response if entry['credit'] < 200]
    print('low_balance')
    print(low_balance)
    
    if session['role'] == 'agent':
        name = user.name

    return render_template(
        'agentportal/dashboard.html',
         user=user, about=about,
        name=name,inactive=inactive,low_balance=low_balance
    )


@core.route('/customer/<int:customer_id>')
def view_customer(customer_id):
    headers = {
        'Content-Type': 'application/json'
    }
    api_url = 'https://app.connexcs.com/api/cp/customer?id=' + str(customer_id)
    # lowbalance_response = requests.get(lowbalance_url)
    response = requests.get(api_url, headers=headers,auth=HTTPBasicAuth(connex_username, connex_password))
    response = response.json() if response.status_code == 200 else []
    print('response')
    print(response[0])
    extension_list = []
    # extensions = response[0]['sip_users']
    # for extension in extensions:
    sip_url = 'https://app.connexcs.com/api/cp/switch/user/?company_id='+str(customer_id)
    # lowbalance_response = requests.get(lowbalance_url)
    sipresponse = requests.get(sip_url, headers=headers,auth=HTTPBasicAuth(connex_username, connex_password))
    sipresponse = sipresponse.json() if sipresponse.status_code == 200 else []
    print(sipresponse)
    for extension in sipresponse:
        # print(extension)
        # print('-------------')
        extension_list.append(extension) 
    # print('extensions')
    # print(len(extension_list))
    return render_template('agentportal/view_customer.html', customer_data=response,extension_list = extension_list)




@core.route('/topup_customer', methods=['POST'])
def topup_customer():
    customer_id = request.form.get('customer_id')
    
    description = request.form.get('description')
    amount = float(request.form.get('amount'))  # Convert amount to float
    print(customer_id)
    print(amount)
    api_url = 'https://app.connexcs.com/api/cp/payment'
    headers = {
        'Content-Type': 'application/json'
    }

    payment_data = {
        'company_id': customer_id,
        'description': description,
        'total': amount,
        'status':'Completed'
    }

    response = requests.post(api_url, json=payment_data, headers=headers, auth=HTTPBasicAuth(connex_username, connex_password))
    response = response.json()
    print(response)
    print(response)
    if response['status'] == 'OK':
        return redirect(url_for('core.view_customer',customer_id=customer_id))
       
    else:
        return jsonify({"error": "Payment failed."})

# @core.route("/delete_siprequests/<int:result_id>", methods=['POST', 'GET'])
# @login_required
# def delete_siprequests(result_id):
#     result = SipRequest.query.get_or_404(result_id)
#     db.session.delete(result)
#     db.session.commit()
#     return redirect(url_for('core.siprequests'))

@core.route("/api/delete_siprequests", methods=['POST', 'GET'])
def delete_siprequests():
    siprequests = request.args.get('siprequests')
    siprequests_list = [int(siprequest) for siprequest in siprequests.split(",")]
    successfully_deleted = []
    failed = []

    for thesiprequest in siprequests_list:
        siprequest = SipRequest.query.filter_by(id=thesiprequest).first()
        if siprequest:
            db.session.delete(siprequest)
            db.session.commit()
            successfully_deleted.append(thesiprequest)
        else:
            failed.append(thesiprequest)

    payload = {
        "status": True,
        "message": " siprequests deleted",
        "successful": successfully_deleted,
        "failed": failed
    }

    return jsonify(payload), 200


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

@core.route("/customersapi", methods=["GET", "POST"])
def resultsapi():
    headers = {
        'Content-Type': 'application/json'
    }
    session.pop('msg', None)
    api_url = 'https://app.connexcs.com/api/cp/customer'
    # response = requests.get(api_url)
    response = requests.get(api_url, headers=headers,auth=HTTPBasicAuth(connex_username, connex_password))
    customers = response.json() if response.status_code == 200 else []
    results_list = []
    print("resultsapi")
    print(customers)

    if customers:
        for result in customers:
            print('res')
       
            payload = {
                "id": result['id'],
                "name": result['name'],
                "credit": result['credit'],
                "ip": result['ips'],
                "debit_limit": result['debit_limit']
                
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
def requestsip():
    form = SipRequestForm()
    user = User.query.filter_by(id=session['id']).first()
    
    if request.method =="POST":
        if request.files.get('certificate'):
            image1 = photos.save(request.files['certificate'], name=secrets.token_hex(10) + ".")
            image1= "static/images/certificates/"+image1
            print("image1")
            print(image1)
        else:
            image1 = "static/images/noimage.JPG"
        siprequest = SipRequest(
            channels=form.channels.data,
            other=form.other.data,
            codecs=form.codecs.data,
            certificate = image1,
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
            "name": "test name",  # You can modify this as per your requirement
            "portal_access": "yes",
            "channels": siprequest.channels,
            "portal_username": "testmail@xyz.com",
            "portal_password":"testmail@xyz.com"

                
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
            "username": "testmail@xyz.com",  # You can modify this as per your requirement
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
        # if request.files.get('certificate'):
        #     image1 = photos.save(request.files['certificate'], name=secrets.token_hex(10) + ".")
        #     image1= "static/images/certificates/"+image1
        #     print("image1")
        #     print(image1)
        # else:
        #     image1 = "static/images/noimage.JPG"

        form_data = request.form.to_dict()
        name = form_data.get('fields[name][value]')
        email = form_data.get('fields[email][value]')
        message = form_data.get('fields[message][value]')
        channels = form_data.get('fields[field_53cf759][value]')
        provider = form_data.get('fields[field_6716889][value]')
        inbound_calls = form_data.get('fields[field_c974d69][value]')
        outbound_calls = form_data.get('fields[field_8fa2d33][value]')
        ip= form_data.get('fields[field_0c54e34][value]')
        certificate =  form_data.get('fields[field_daeacb9][value]')
        print(name)
        print(request)
        print(request.args)
        print(request.form)
        print("name")
        print(request.args.get('name'))
        print(request.form.get('name'))
        
        
        customer_data = {
            "name": name,
            "portal_access": "yes",
            "channels": channels,
            "portal_username": email,
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
            "name":name,
            "contact_type":"General",
            "email": email,
              "password":customer_data['portal_password'],
              "company_id": create_customer_response_data["id"],
            # Include other SIP user data fields as needed
        }
        
        create_contact = requests.post(
            "https://app.connexcs.com/api/cp/contact",
            json=contact_data,
            headers=headers,
            auth=HTTPBasicAuth(connex_username, connex_password)
        )
        print("contact info")
        print(create_contact.content)
        sip_request = SipRequest(
            channels = channels,
            other = message,
            codecs = channels,
            inbound = inbound_calls,
            outbound = outbound_calls,
            provider = provider,
            name = name,
            email = email,
            customer_id = create_customer_response_data["id"],
            certificate = certificate,
            ip = ip 

        )
        
        db.session.add(sip_request)
        db.session.commit()
        msg = Message(
        sender = "info@delaphonegh.com",
        subject="Delaphone Portal Information",
        recipients=[sip_request.email],
        # recipients=['raymondvaughanwilliams@gmail.com'],
        # html="<p>Package has been created.<p>Details:<br><ul><li>Item:{}</li><li>Sender Location:{}</li><li>Destination:{}</li><li>Price:{}</li><li>Start Date:{}</li><li>End Date:{}</li></ul>".format( form.item_description.data,  delivery.sender_location.name,delivery.sender_location.name,delivery.price,form.start_date.data,form.end_date.data)
        html= render_template('mails/welcome.html', sip_request=sip_request,password=password )

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
        context = {
            "status": True,
            "message": " Customer Created!",
        }

        return 200
        # return jsonify({"message": "Success"})
    
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
                "other":siprequest.other,
                "certificate":siprequest.certificate,
                "status":siprequest.status,
                "ip":siprequest.ip
             
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
                "channel": result.channels,
                "codecs": result.codecs.name,
                "inbound": result.inbound,
                "outbound": result.outbound,
                "provider":result.provider,
                "status":result.status
                
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




@core.route("/siprequests", methods=["GET", "POST"])
@login_required
def siprequests():
    form = FilterForm()
    page = request.args.get('page', 1, type=int)
    siprequests = SipRequest.query.all()


    
    return render_template(
        "agentportal/siprequests.html",
        siprequests=siprequests,
        form=form, page=page,
        
    )



@core.route("/customers", methods=["GET", "POST"])
@login_required
def customers():
    form = FilterForm()
    page = request.args.get('page', 1, type=int)
    customers = SipRequest.query.all()


    
    return render_template(
        "agentportal/customers.html",
        
        form=form, page=page,
        
    )

@core.route("/editsiprequest/<int:id>", methods=["POST", 'GET'])
@login_required
def editsiprequest(id):
    form = SipRequestForm()
    result = SipRequest.query.filter_by(id=id).first()
    password= generate_secure_password()
    random_number = random.randint(1, 10) 
    if request.method == "POST":
        print('in post')
        result.channels = form.channels.data
        # result.subject = form.subject.data
        result.codecs = form.codecs.data
        result.provider = form.provider.data
        result.status = form.status.data
        result.ip = form.ip.data
   

        db.session.commit()
   
        

        company_id = result.customer_id
        card_id = form.ratecard.data
        print(company_id)
        api_url = f'https://app.connexcs.com/api/cp/routing'
        params = {
            'company_id': company_id,
            'card_id': card_id
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(api_url, params=params, headers=headers, auth=HTTPBasicAuth(connex_username, connex_password))
        routing_info = response.json() if response.status_code == 200 else {}
        print('routing_info')
        print(routing_info)
        print(response.content)

        if form.status.data == 'verified' and form.create_extension.data=='yes':
            print('Creating new extension for user...')

            headers = {
                "Content-Type": "application/json"
            }
            
            extension_data = {
                "username":result.name + str(random_number) ,
                "password":password,
                "channels": result.channels,
                "ip_whitelist":result.ip,
                "company_id": result.customer_id,
                # Include other SIP user data fields as needed
            }
            
            create_extension = requests.post(
                "https://app.connexcs.com/api/cp/switch/user",
                json=extension_data,
                headers=headers,
                auth=HTTPBasicAuth(connex_username, connex_password)
            )
            print("contact info")
            print(create_extension.content)

            

            # extension = Extension(
            # password=form.password.data,
            # channels=result.channels,
            # ip_whitelist=result.ip,
            # company_id = result.customer_id,
            # siprequest_id = result.siprequest_id,
            # )
            # db.session.add(extension)
            # db.session.commit() 

            return redirect(url_for("core.siprequests"))
        else:
            return redirect(url_for("core.siprequests"))

    # elif request.method == 'GET':
    #     form.name.data = result.name
    #     form.subject.data = result.subject
    #     form.result.data = result.result
      

    return render_template("agentportal/siprequests.html", result=result, form=form)


#EMERGENT/CE AIRTIME API

#API URLS. USE Variables cos you have to change them later  https://testsrv.interpayafrica.com/v7/Airtime.svc
EMERGENCE_API_URL = 'https://testsrv.interpayafrica.com/v7/Airtime.svc/topup'
EMERGENCE_API_URL_MOMO = 'https://testsrv.interpayafrica.com/v7/Airtime.svc/topupbymm'
EMERGENCE_API_URL_BANK = 'https://testsrv.interpayafrica.com/v7/Airtime.svc/topupbybankacct'

#Any payment platform? 
def perform_any_request(form_data):
    print(form_data)
    print(form_data['type'])
    topup_params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'payername': form_data['payername'],
        'payermobile': form_data['payermobile'],
        'payeremail': form_data.get('payeremail'),
        'recipientmobile': form_data['recipientmobile'],
        'amount': form_data['amount'],
        'merchtxnref': form_data['merchtxnref'],
        'countryid': form_data['countryid'],
        'oprid': form_data['oprid']
    }
    
    response = requests.post(EMERGENCE_API_URL, json=topup_params)
    print("response")
    print(response.content)
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        return {"error": "API request failed"}

#Momo payments
def perform_momo_request(form_data):
    momo_params = {
        'app_id': form_data['app_id'],
        'app_key': form_data['app_key'],
        'payername': form_data['payername'],
        'payermobile': form_data['payermobile'],
        'payeremail': form_data.get('payeremail'),
        'payercountryid': form_data['payercountryid'],
        'payeroprid': form_data['payeroprid'],
        'recipientmobile': form_data['recipientmobile'],
        'vouchernumber': form_data.get('vouchernumber'),
        'amount': form_data['amount'],
        'merchtxnref': form_data['merchtxnref']
    }
    
    response = requests.post(EMERGENCE_API_URL_MOMO, data=momo_params)
    
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        return {"error": "API request failed"}
    
#Bank topups
def perform_bank_topup_request(form_data):
    bank_topup_params = {
        'app_id': APP_ID,
        'app_key': APP_KEY,
        'payername': form_data['payername'],
        'payermsisdn': form_data.get('payermsisdn'),
        'payeremail': form_data.get('payeremail'),
        'payerbankacctno': form_data['payerbankacctno'],
        'payerbankaccttitle': form_data['payerbankaccttitle'],
        'bankbranchsortcode': form_data['bankbranchsortcode'],
        'recipientmsisdn': form_data['recipientmsisdn'],
        'amount': form_data['amount'],
        'merchtxnref': form_data['merchtxnref'],
        'countryid': form_data['countryid'],
        'oprid': form_data['oprid']
    }
    
    response = requests.post(EMERGENCE_API_URL_BANK, data=bank_topup_params)
    
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        return {"error": "API request failed"}


#Topup route/api
@core.route('/api/topup', methods=['POST'])
def topup_route():
    if request.method == 'POST':
        if 'type' in request.form:
            if request.form['type'] == 'topup':
                response = perform_any_request(request.form)
                return jsonify(response)
            elif request.form['type'] == 'momo':
                response = perform_momo_request(request.form)
                return jsonify(response)
            elif request.form['type'] == 'bank':
                response = perform_momo_request(request.form)
                return jsonify(response)
            else:
                return jsonify({"error": "Invalid type value"})
            # airtimetopup = AirtimeTopup(payername)
        else:
            return jsonify({"error": "Missing type field"})
    else:
        return jsonify({"error": "Method not allowed"})



from datetime import datetime

@core.route('/api/cdr', methods=['POST'])
def cdrapi():
    print("request")
    print(request)
    password = generate_secure_password()
 
    if request.method == 'POST':
        # if request.files.get('certificate'):
        #     image1 = photos.save(request.files['certificate'], name=secrets.token_hex(10) + ".")
        #     image1= "static/images/certificates/"+image1
        #     print("image1")
        #     print(image1)
        # else:
        #     image1 = "static/images/noimage.JPG"
        data = request.json
        date_time = datetime.strptime(data.get('DateTime'), '%Y-%m-%dT%H:%M:%S')
        call_start_time_local = datetime.strptime(data.get('CallStartTimeLocal'), '%Y-%m-%dT%H:%M:%S')
        call_start_time_utc = datetime.strptime(data.get('CallStartTimeUTC'), '%Y-%m-%dT%H:%M:%S')
        call_established_time_local = datetime.strptime(data.get('CallEstablishedTimeLocal'), '%Y-%m-%dT%H:%M:%S')
        call_established_time_utc = datetime.strptime(data.get('CallEstablishedTimeUTC'), '%Y-%m-%dT%H:%M:%S')
        call_end_time_local = datetime.strptime(data.get('CallEndTimeLocal'), '%Y-%m-%dT%H:%M:%S')
        call_end_time_utc = datetime.strptime(data.get('CallEndTimeUTC'), '%Y-%m-%dT%H:%M:%S')


        call_type = request.json.get('CallType')
        number = request.json.get('Number')
        call_direction = request.json.get('CallDirection')
        name = request.json.get('Name')
        entity_id = request.json.get('EntityId')
        entity_type = request.json.get('EntityType')
        queue_extension = request.json.get('QueueExtension')
        agent = request.json.get('Agent')
        agent_first_name = request.json.get('AgentFirstName')
        agent_last_name = request.json.get('AgentLastName')
        agent_email = request.json.get('AgentEmail')
        duration = request.json.get('Duration')
        duration_timespan = request.json.get('DurationTimespan')
        # ... (Retrieve other fields using request.json.get)
        print(request.json)

        cdr = CDR(
            call_type=call_type,
            number=number,
            call_direction=call_direction,
            name=name,
            entity_id=entity_id,
            entity_type=entity_type,
            queue_extension=queue_extension,
            agent=agent,
            agent_first_name=agent_first_name,
            agent_last_name=agent_last_name,
            agent_email=agent_email,
            duration=duration,
            duration_timespan=duration_timespan,
            # ... (Assign other fields)
            date_time=date_time,
            call_start_time_local=call_start_time_local,
            call_start_time_utc=call_start_time_utc,
            call_established_time_local=call_established_time_local,
            call_established_time_utc=call_established_time_utc,
            call_end_time_local=call_end_time_local,
            call_end_time_utc=call_end_time_utc,
            call_start_time_local_millis=request.json.get('CallStartTimeLocalMillis'),
            call_start_time_utc_millis=request.json.get('CallStartTimeUTCMillis'),
            call_established_time_local_millis=request.json.get('CallEstablishedTimeLocalMillis'),
            call_established_time_utc_millis=request.json.get('CallEstablishedTimeUTCMillis'),
            call_end_time_local_millis=request.json.get('CallEndTimeLocalMillis'),
            call_end_time_utc_millis=request.json.get('CallEndTimeUTCMillis'),
            subject=request.json.get('Subject'),
            inbound_call_text=request.json.get('InboundCallText'),
            missed_call_text=request.json.get('MissedCallText'),
            outbound_call_text=request.json.get('OutboundCallText'),
            not_answered_outbound_call_text=request.json.get('NotAnsweredOutboundCallText')
   
        )

        db.session.add(cdr)
        db.session.commit()

        return jsonify({"message": "CDR saved successfully."})
        
        # context = {
        #     "status": True,
        #     "message": " CDR saved successfully",
        # }

        # return 200
        # # return jsonify({"message": "Success"})
    
    return "Welcome to the SIP Request API"




@core.route('/contact_lookup', methods=['GET'])
# @require_api_key
def contactlookup():
   
    number = request.args.get('phone_mobile')
    print(request.args.get('phone_mobile'))
    
    print(number)
    if(request.args.get('phone_mobile')):
        number = number.strip().replace("'","")
        contact = Contact.query.filter_by(phone_mobile=number).first()
        
    elif(request.args.get('email')):
        contact = Contact.query.filter_by(email=request.args.get('email')).first()
    else:
        contact  = None
    contacts = Contact.query.all()
    print(contact)
    print(contacts)
    if contact is not None:
        
        # ecom_request = EcomRequest(
        #     number=number,
        #     farmer_id=farmer.id,
        #     disposition="200",
        #     sms_disposition=res[0]
        # )

        # db.session.add(ecom_request)
        # db.session.commit()
        print('contact exists')
        payload = {
            'id': contact.id,
            "True": True,
            "firstName": contact.first_name,
            "lastName": contact.last_name,
            "phone_mobile": contact.phone_mobile,
            "email":contact.email
        }

        context = {
            "status": True,
            "message": " Contact found",
            "data": payload
        }
        return jsonify(context), 200

    else:
        print('contact doesnt exist')
        # ecom_request = EcomRequest(
        #     number=number,
        #     farmer_id=None,
        #     disposition="404",
        #     sms_disposition="No sms sent",
        # )

        # db.session.add(ecom_request)
        # db.session.commit()
        context = {
            "status": False,
            "message": "Contact not found",
            "error": "null"
        }

        return jsonify(context), 404


# scheduler = BackgroundScheduler()
# scheduler.add_job(func=resend_sms, trigger="interval", seconds=600)
# scheduler.start()
# atexit.register(lambda: scheduler.shutdown())
