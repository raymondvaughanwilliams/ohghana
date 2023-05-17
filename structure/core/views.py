from flask import render_template,Blueprint,session,redirect,url_for,jsonify,current_app,request,send_file
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
from os import environ

core = Blueprint('core', __name__)

API_KEY = os.environ.get('API_KEY')


def farmer_to_dict(farmer):
    """ Converts a farmer model to a dictionary """
    return {
        'id': farmer.id,
        'first_name': farmer.first_name,
        'last_name': farmer.last_name,
        'number': farmer.number,
        'premium_amount': farmer.premium_amount,
        'location': farmer.location,
        'country': farmer.country,
        'cashcode': farmer.cashcode,
        'date_added': farmer.date_added,
        'last_modified': farmer.last_modified,
        'language': farmer.language,
        'society': farmer.society,
        'farmercode': farmer.farmercode,
        'cooperative': farmer.cooperative,
        'ordernumber': farmer.ordernumber
    }


def require_api_key(view_function):
    def decorated_function(*args, **kwargs):
        if request.headers.get('Authorization') == API_KEY:
            return view_function(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid API key', 'status': False}), 401

    return decorated_function

def generate_csv_content(duplicates):
    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(['Cooperative', 'Farmer Code', 'Last Name', 'Society', 'Number', 'Premium Amount', 'Language', 'Cash Code', 'Country'])
    csv_writer.writerows(duplicates)
    return output.getvalue()

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
    # session.pop('uploaded',None)
    # session.pop('duplicates',None)
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)
    name="ecom"
    session.pop('msg',None)
    
    farmers = Farmer.query.order_by(desc(Farmer.id)).all()
    # ecomrequests  = EcomRequest.query.all()
    ecomrequests = EcomRequest.query.order_by(desc(EcomRequest.id)).all()

    form = FilterForm()
    if session['role'] == 'agent':
        name = user.name
        # print(op)

    return render_template('agentportal/dashboard.html', form=form, user=user, about=about, name=name, farmers=farmers,
                           ecomrequests=ecomrequests)


@core.route('/claims', methods=['GET', 'POST'])
@login_required
def claims():
    user = User.query.filter_by(id=session['id']).first()
    about = About.query.get(1)

    ecomrequests = EcomRequest.query.all()

    form = FilterForm()

    name = user.name

    if request.method == "POST":
        # Get the filter values from the form
        first_name = form.first_name.data
        print(first_name)
        last_name = form.last_name.data

        location = form.location.data
        number = form.number.data
        cooperative = form.cooperative.data
        language = form.language.data
        country = form.country.data
        society = form.society.data

        # Build the SQLAlchemy filter conditions
        conditions = []
        if first_name:
            first_name_conditions = [
                EcomRequest.farmers.first_name.like(f"%{first_name}%"),
                EcomRequest.farmers.first_name.like(f"{first_name}%"),
                EcomRequest.farmers.first_name.like(f"%{first_name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*first_name_conditions))
        if last_name:
            last_name_conditions = [
                EcomRequest.farmers.last_name.like(f"%{last_name}%"),
                EcomRequest.farmers.last_name.like(f"{last_name}%"),
                EcomRequest.farmers.last_name.like(f"%{last_name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*last_name_conditions))
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
                EcomRequest.location.like(f"%{location}%"),
                EcomRequest.location.like(f"{location}%"),
                EcomRequest.location.like(f"%{location}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the destination variations
            conditions.append(or_(*location_conditions))
        if cooperative:
            cooperative_conditions = [
                EcomRequest.cooperative.like(f"%{cooperative}%"),
                EcomRequest.cooperative.like(f"{cooperative}%"),
                EcomRequest.cooperative.like(f"%{cooperative}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*cooperative_conditions))
        if society:
            society_conditions = [
                EcomRequest.society.like(f"%{society}%"),
                EcomRequest.society.like(f"{society}%"),
                EcomRequest.society.like(f"%{society}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*society_conditions))
        if country:
            country_conditions = [
                EcomRequest.country.like(f"%{country}%"),
                EcomRequest.country.like(f"{country}%"),
                EcomRequest.country.like(f"%{country}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*country_conditions))

        print(conditions[0])
        ecomrequests = EcomRequest.query.filter(and_(*conditions)).all()
        print(ecomrequests)

    # print(op)

    return render_template('agentportal/claims.html', form=form, ecomrequests=ecomrequests, filterform=form)


@core.route("/addfarmer", methods=["GET", "POST"])
@login_required
def addfarmer():
    form = FarmerForm()
    items = Farmer.query.all()
    if request.method == "POST":
        check_farmer = Farmer.query.filter_by(number=form.number.data).first()
        if check_farmer:
            session['msg'] = "Farmer already exists"
            return redirect(url_for("core.addfarmer"))
        else:

            farmer = Farmer( first_name="NA",last_name=form.last_name.data, number=form.number.data,premium_amount=form.premium_amount.data,location="NA",language=form.language.data,country=form.country.data,cooperative=form.cooperative.data,ordernumber="NA",cashcode=form.cashcode.data,society=form.society.data)
            db.session.add(farmer)
            db.session.commit()
            return redirect(url_for("core.farmers"))
    return render_template("agentportal/addfarmer.html",form=form,items=items)


def farmer_to_dict(item):
    return {
        'id': item.id,
        'first_name': item.first_name,
        'last_name': item.last_name,
        'number': item.number,
        'premium_amount': item.premium_amount,
        'location': item.location,
        'country': item.country,
        'cashcode': item.cashcode,
        'date_added': item.date_added,
        'last_modified': item.last_modified,
        'language': item.language,
        'society': item.society,
        'farmercode': item.farmercode,
        'cooperative': item.cooperative,
        'ordernumber': item.ordernumber
    }


@core.route("/farmers", methods=["GET", "POST"])
@login_required
def farmers():
    form = FilterForm()
    page = request.args.get('page', 1, type=int)
    farmers = Farmer.query.paginate(page, 10, False)
    session.pop('msg',None)
    # session.pop('uploaded',None)
    # session.pop('duplicates',None)
      search="no"
    if request.method == "POST":
        search = "yes"
        # Get the filter values from the form
        first_name = form.first_name.data
        print(first_name)
        last_name = form.last_name.data
        location = form.location.data
        number = form.number.data
        cooperative = form.cooperative.data
        language = form.language.data
        country = form.country.data
        society = form.society.data

        # Build the SQLAlchemy filter conditions
        conditions = []
        if first_name:
            first_name_conditions = [
                Farmer.first_name.like(f"%{first_name}%"),
                Farmer.first_name.like(f"{first_name}%"),
                Farmer.first_name.like(f"%{first_name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*first_name_conditions))
        if last_name:
            last_name_conditions = [
                Farmer.last_name.like(f"%{last_name}%"),
                Farmer.last_name.like(f"{last_name}%"),
                Farmer.last_name.like(f"%{last_name}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*last_name_conditions))
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
        if cooperative:
            cooperative_conditions = [
                Farmer.cooperative.like(f"%{cooperative}%"),
                Farmer.cooperative.like(f"{cooperative}%"),
                Farmer.cooperative.like(f"%{cooperative}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*cooperative_conditions))
        if society:
            society_conditions = [
                Farmer.society.like(f"%{society}%"),
                Farmer.society.like(f"{society}%"),
                Farmer.society.like(f"%{society}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*society_conditions))
        if country:
            country_conditions = [
                Farmer.country.like(f"%{country}%"),
                Farmer.country.like(f"{country}%"),
                Farmer.country.like(f"%{country}"),
            ]
            # Use the OR operator to combine the conditions into a single
            # condition that matches any of the location variations
            conditions.append(or_(*country_conditions))

        # print(conditions[0])
        # else:

        farmers = Farmer.query.filter(and_(*conditions)).all()
        print(farmers)
    # user = User.query.filter_by(id=session['id']).first()

    return render_template("agentportal/farmers.html", farmers=farmers, form=form, filterform=form, page=page,
                           search=search)


@core.route("/farmer/<int:id>", methods=["POST", 'GET'])
@login_required
def farmer(id):
    form = FarmerForm()
    farmer = Farmer.query.filter_by(id=id).first()
    farmers = Farmer.query.all()

    if request.method == "POST":
        farmer.first_name = form.first_name.data
        farmer.last_name = form.last_name.data
        farmer.number = form.number.data
        farmer.premium_amount = form.premium_amount.data
        farmer.country = form.country.data
        farmer.language = form.language.data
        farmer.society = form.society.data
        farmer.cooperative = form.cooperative.data
        farmer.cashcode = form.cashcode.data
        # bid.status = 'bid'

        db.session.commit()

        return redirect(url_for("core.farmers"))

    elif request.method == 'GET':
        form.first_name.data = farmer.first_name
        form.last_name.data = farmer.last_name
        form.number.data = farmer.number
        form.premium_amount.data = farmer.premium_amount
        form.language.data = farmer.language
        form.society.data = farmer.society
        form.country.data = farmer.country
        form.cooperative.data = farmer.cooperative
        form.cashcode.data = farmer.cashcode

    return render_template("agentportal/farmer.html", farmer=farmer, form=form)







@core.route('/uploadfarmer',methods=['GET', 'POST'])
@login_required
def uploadfarmer():
    form = FarmerForm()
    user = User.query.filter_by(email=session['email']).first()
    user_id = user.id
    session.pop('msg',None)
    
    data= []

    if form.validate_on_submit():
        if form.uploadfile.data:

            uploaded_file = request.files['uploadfile']
            print("file")
            print(uploaded_file.filename)
            filepath = os.path.join(current_app.root_path, uploaded_file.filename)
            uploaded_file.save(filepath)
            with open(filepath, encoding='ISO-8859-1') as file:
                csv_file = csv.reader(file)
                upload_data = []
                tdata = []
                print(csv_file)
                next(csv_file)
                line_count= 0
                for row in csv_file:
                    upload_data.append(row)
                #     line_count += 1
                #     try:
                #         print("saving")
                #         # farmers_save = Farmer(first_name=row[0],last_name=row[1],number=row[2])
                #         farmers_save = Farmer(cooperative=row[0],farmercode=row[1],last_name=row[2],society=row[3],number=row[4],premium_amount=row[7],language=row[8],cashcode=row[9],country=row[10],first_name="NA",location="NA")
                #         print("saved")
                #         tdata.append(row) 

                #     except Exception as e:
                #         # Add the line number to the error message
                #         error_message = f"Error on line {line_count}: {str(e)}"
                #         # Handle the error appropriately
                #         message = error_message
                #         print(message)

                session['csv_data'] = upload_data
                    
                print(upload_data)
                return  redirect(url_for('core.uploadsummary'))
        # else:
        #     farmers_save = Farmer(code=form.code.data,cost=form.cost.data,country=form.country.data,route=form.route.data)
        #     db.session.add(farmers_save)
        #     db.session.commit()
    return render_template('agentportal/uploadfarmer.html',form=form,user=user,data=data)

@core.route('/uploadsummary', methods=['GET','POST'])
def uploadsummary():
    form = FarmerForm()
    data = session['csv_data']
    print('...')
    print(data)
    if request.method=='POST':
        uploaded = []
        duplicates=[]
        print('saving')
        line_count = 0
        print("len")
        print(len(data))
        for i in range(0, len(data)):
            print("in range")
            print("saving")
            farmer = Farmer.query.filter_by(number =data[i][4]).first()
            

            if farmer:
                print("duplicate found")
                duplicates.append(data[i])
            else:
                try:
            # farmers_save = Farmer(first_name=row[0],last_name=row[1],number=row[2])
                    farmers_save = Farmer(cooperative=data[i][0],farmercode=data[i][1],last_name=data[i][2],society=data[i][3],number=data[i][4],premium_amount=data[i][5],language=data[i][6],cashcode=data[i][7],country=data[i][8],first_name="NA",location="NA")
                    db.session.add(farmers_save)
                    db.session.commit()
                    uploaded.append(data[i])
                    print("saved")
            

                except Exception as e:
                    # Add the line number to the error message
                    error_message = f"Error on line {line_count}: {str(e)}"
                    # Handle the error appropriately
                    message = error_message
                    print(message)
                    session.pop('csv_data',None)
        session['uploaded_farmers'] = uploaded
        session['duplicates'] = duplicates
        return redirect(url_for('core.uploadsummarydetails'))

    return render_template('agentportal/uploadsummary.html',len_added=len(data),data=data,form=form)

@core.route('/uploadsummarydetails', methods=['GET','POST'])
def uploadsummarydetails():
    print(session)
    duplicates = session['duplicates']
    uploaded = session['uploaded_farmers']
    return render_template('agentportal/uploadsummarydetails.html',len_added=len(uploaded),uploaded=uploaded,len_duplicates=len(duplicates),duplicates=duplicates)


@core.route("/delete_farmer/<int:farmer_id>", methods=['POST', 'GET'])
@login_required
def delete_farmer(farmer_id):
    farmer = Farmer.query.get_or_404(farmer_id)
    db.session.delete(farmer)
    db.session.commit()
    return redirect(url_for('core.farmers'))


@core.route('/api/addfarmer', methods=['GET', 'POST'])
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
                  last_name=last_name, number=number, location=location
                  )
    db.session.add(farmer)
    db.session.commit()
    status = 1
    if status == 1:
        return jsonify(first_name, last_name, premium_amount, "success")
    else:
        return jsonify("Failed")


@core.route('/api/senddemosms', methods=['GET', 'POST'])
# @require_api_key
def senddemosms():
    # print(request.args.get('number'))

    # number = requests.json['number']
    number = request.args.get('number')
    print("number")
    print(number[1:])

    url = 'http://rslr.connectbind.com:8080/bulksms/bulksms'
    # apiKey =
    rpassword = environ.get('ROUTESMS_PASS')
    data = {
        'username': 'dlp-testacc',
        'password': rpassword,
        'type': '0',
        'dlr': '1',
        'destination': number[1:],
        'source': 'test',
        'message': 'Welcome to Delaphone’s Cloud Answering Service, partner with us to optimize your customer experience'
    }
    response = requests.post(url, data)

    # response_data = response.json()
    # print("response_data")
    res = response.text.split("|")
    print(res)
    print(res)

    payload = {"True": True,
               "res": res
               }
    context = {"status": True,
               "message": " Message triggered",
               "data": payload
               }
    return jsonify(context)


@core.route('/api/checknumber', methods=['GET', 'POST'])
# @require_api_key
def checknumber():
    # print(request.args.get('number'))

    # number = requests.json['number']
    number = request.args.get('number')
    number = number.strip()
    print("Checking for number:")
    print(number)

    farmer = Farmer.query.filter_by(number=number).first()
    if farmer is not None:

        ecomrequest = EcomRequest(number=number, country=farmer.country, farmer_id=farmer.id, cashcode=farmer.cashcode)
        db.session.add(ecomrequest)
        db.session.commit()

        # endPoint = 'https://api.mnotify.com/api/sms/quick'
        # # apiKey =
        if farmer.country == "Ghana":
            message = "Hello " + farmer.last_name + " . Your 2022/2023 premium is GHS" + str(
                farmer.premium_amount) + ". Your cash code is " + str(farmer.cashcode) + ".  Thank you,ECOM."
        else:
            message ="Bonjour " + farmer.last_name +" votre prime 2022/2023 est CFA" + str(farmer.premium_amount) + ". Votre code de caisse est "+ " "+ str(farmer.cashcode)+". Merci, Zamacom."
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
            'type': '0',
            'dlr': '1',
            'destination': number,
            'source': 'test',
            'message': message
        }

        # --------------------------------
        response = requests.post(url, data)

        # response_data = response.json()
        # print("response_data")
        res = response.text.split("|")
        print(res)

        payload = {"True": True, "firstName": farmer.first_name,
                   "lastName": farmer.last_name,
                   "premium_amount": farmer.premium_amount,
                   "location": farmer.location
                   }
        context = {"status": True,
                   "message": " Farmer found",
                   "data": payload
                   }
        return jsonify(context), 200
    else:
        context = {"status" :False,
        "message":"Farmer not found",
        "error": "null"}
        return jsonify(context),404
    


@core.route('/download-duplicates')
def download_duplicates():
    # Retrieve the duplicates from the session
    duplicates = session.get('duplicates')
    # Generate a CSV file containing the duplicates
    csv_content = generate_csv_content(duplicates)
    # Create a temporary file to store the CSV content
    temp_file = 'duplicates.csv'
    with open(temp_file, 'w') as file:
        file.write(csv_content)
    # Return the file for download
    return send_file(temp_file, as_attachment=True, attachment_filename='duplicates.csv')
