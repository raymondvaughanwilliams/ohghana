import re
from flask import render_template,url_for,flash, redirect,request,Blueprint,session
from flask_login import current_user,login_required
from structure import db
from structure.models import Price, User ,Payment
from structure.pricing.forms import PriceForm
import random

pricings = Blueprint('pricings',__name__)

@pricings.route('/create_price',methods=['GET','POST'])
@login_required
def create_post():
    form = PriceForm()

    if request.method == 'POST':

        pricing = Price(title=form.title.data,
                             amount=form.amount.data,
                             features=form.features.data,
                             )
        db.session.add(pricing)
        db.session.commit()
        flash("Pricing Created")
        return redirect(request.args.get('next') or request.referrer )


    return render_template('create_price.html',form=form)


# int: makes sure that the price_id gets passed as in integer
# instead of a string so we can look it up later.
@pricings.route('/plan/<int:plan_id>')
def plan(plan_id):
    # grab the requested blog post by id number or return 404
    user = User.query.filter_by(email=session['email']).first()
    rem_sessions = user.rem_sessions
    rem_chatweeks = user.rem_chatweeks
    price = Price.query.get_or_404(plan_id)
    return render_template('plan.html',title=price.title,
                            amount=price.amount,features=price.features,price=price,rem_sessions=rem_sessions,rem_chatweeks=rem_chatweeks
    )

@pricings.route("/<int:price_id>/update_pricing", methods=['GET', 'POST'])
@login_required
def update_pricing(price_id):
    price = Price.query.get_or_404(price_id)

    form = PriceForm()
    if request.method == 'POST':
        price.title = form.title.data
        price.amount = form.amount.data
        price.features = form.features.data
        db.session.commit()
        flash('Post Updated')
        return redirect(request.args.get('next') or request.referrer )

    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = price.title
        form.amount.data = price.amount
        form.features.data = price.features
    return render_template('update_price.html', title='Update',
                           form=form,price=price)





@pricings.route("/pricings/<int:id>", methods=['GET', 'POST'])
@login_required
def allprices(id):

    pricing = Price.query.all()
    tid = id
    # if pricing:
    #     title = pricing.title
    #     amount = pricing.amount
    #     features = pricing.features
    #     services=[]
    #     service= pricing.features.split(',')
    #     services.append(service)
    return render_template('pricing-page.html',pricing=pricing,tid=tid)

   

@pricings.route("/<int:price_id>/delete_post", methods=['POST','GET'])
@login_required
def delete_post(price_id):
    pricing = Price.query.get_or_404(price_id)
    db.session.delete(pricing)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))




@pricings.route("/buyplan/<int:id>/<int:tid>")
@login_required
def buyplan(id,tid):
    price = Price.query.get_or_404(id)
    userdemail = session['email']
    user =  User.query.filter_by(email=userdemail).first()
    name = user.name
    number = user.number
    # random_num = randint(1,1000)
    tx_ref = user.email[0:6]+ str(random.randint(1,1000))
    tid = tid
    return render_template('buyplan.html',price=price,useremail=userdemail,tx_reff=tx_ref,name=name,number=number,tid=tid)


@pricings.route("/confirmplan/<int:id>")
@login_required
def confirmplan(id):
    price = Price.query.get_or_404(id)
    loggeduser = session['email']
    print("ogged:")
    print(loggeduser)
    user = User.query.filter_by(email=loggeduser).first()
            # user = User.query.filter_by(email=form.email.data).first()

    print(user)
    user.plan_id = id
    user.rem_sessions = price.numsessions
    user.rem_chatweeks = price.numchatweeks
    db.session.commit()

    return redirect(url_for('core.index'))




@pricings.route("/paymentdetails/<int:id>")
@login_required
def paymentdetails(id):
    price = Price.query.get_or_404(id)
    loggeduser = session['email']
    print("ogged:")
    print(loggeduser)
    user = User.query.filter_by(email=loggeduser).first()
            # user = User.query.filter_by(email=form.email.data).first()

    print(user)
    user.plan_id = id
    user.rem_sessions = price.numsessions
    user.rem_chatweeks = price.numchatweeks
    db.session.commit()

    return render_template('payment-details-drop-down.html')



@pricings.route("/confirmravepayment")
@login_required
def confirmravepayment():
    user = User.query.filter_by(email=session['email']).first()
    uid = user.id
    
    if request.args.get('status') == "successful":
        transaction_id = request.args.get('transaction_id')
        # user = User.query.filter_by(email=session['email']).first()
        status = request.args.get('status')
        tx_ref = request.args.get('tx_ref')
        amount = request.args.get('amount')
        tid = request.args.get('tid')
        print(tid)
        amount_dict = amount.split(' ')
        price = amount_dict[0]
        plan = Price.query.filter_by(amount=amount).first()

        user.rec_transaction_id = transaction_id
        user.plan_id = plan.id
        user.therapist_id = tid



        print(plan.title)
        print(amount_dict)
        print(amount)
        payment = Payment(transaction_id=transaction_id,
                             tx_ref=tx_ref,
                             user_id =uid,status=status,amount=price,plan_id = plan.id
                             )
        db.session.add(payment)
        db.session.commit()

        flash("Pricing Created")
        return redirect(url_for('pricings.paymentconfirmation'))




    #     if request.status == "successful":
    #         print("payment successful")
    #     else:
    #         print("payment rejected")
    # print(request.url)
    # status = request.args.get('status')
    # print(username)

    # user = User.query.filter_by(email=loggeduser).first()
    #         # user = User.query.filter_by(email=form.email.data).first()

    # print(user)
    # user.rem_sessions = price.numsessions
    # user.rem_chatweeks = price.numchatweeks
    # db.session.commit()

    return redirect(url_for('core.index'))




@pricings.route("/paymentconfirmati/")
@login_required
def paymentconfirmati():

    return render_template('plan-succesful.html')