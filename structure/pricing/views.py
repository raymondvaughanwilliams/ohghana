from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from structure import db
from structure.models import Price
from structure.pricing.forms import PriceForm

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
@pricings.route('/<int:price_id>')
def price(price_id):
    # grab the requested blog post by id number or return 404
    price = Price.query.get_or_404(price_id)
    return render_template('price.html',title=price.title,
                            amount=price.amount,features=price.features,price=price
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





@pricings.route("/pricings", methods=['GET', 'POST'])
@login_required
def allprices():

    pricing = Price.query.all()

    if pricing:
        title = pricing.title
        amount = pricing.amount
        features = pricing.features
        services=[]
        service= pricing.features.split(',')
        services.append(service)
        return render_template('base2.html',pricing=pricing,title=title,amount=amount,services=services)

   

@pricings.route("/<int:price_id>/delete_post", methods=['POST','GET'])
@login_required
def delete_post(price_id):
    pricing = Price.query.get_or_404(price_id)
    db.session.delete(pricing)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))