# users/views.py
from flask import render_template,url_for,flash,redirect,request,Blueprint,session
from flask_login import login_user, current_user, logout_user, login_required
from structure import db,photos,mail 
from structure.models import User 
from structure.users.forms import RegistrationForm,LoginForm,UpdateUserForm
from structure.users.picture_handler import add_profile_pic
import secrets
import requests
import os
from requests.auth import HTTPBasicAuth
from flask_mail import Mail, Message
from structure.core.views import generate_secure_password
import random

users = Blueprint('users',__name__)



connex_username = os.environ.get('connex_username')
connex_password = os.environ.get('connex_password')
# register
@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    print("hghgj")
    # if form.validate_on_submit():
    if request.method == 'POST':
        print("df")
        user = User(email=form.email.data,
                    name=form.name.data,
                    username=form.username.data,
                    password=form.password.data,
                    last_name=form.last_name.data,role="user",
                    number=form.number.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering!')
        if user.role == 'user':
            session['id'] = user.id
            return redirect(url_for('users.enterartist'))
        else:
            return redirect(url_for('users.vendorregister',id=user.id))
            

    return render_template('user/signup.html',form=form)













@users.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        
        userr = User.query.filter_by(email=form.email.data).first()
        


        if user is not None and user.check_password(form.password.data)  :
            #Log in the user
            session['name'] = userr.name
            session['role'] = userr.role
            session['email'] = form.email.data
            session['id'] = user.id
            session['username'] = user.username
            print("session")
            print(session['name'])
            login_user(user)
            flash('Logged in successfully.')




            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.dashboard')
            

            return redirect(next)
        else:
            session['loginmsg'] = "Invalid credentials. Try again"
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('core.dashboard')
            

            return redirect(next)




    return render_template('user/signin.html', form=form)

# logout
@users.route("/logout")
def logout():
    logout_user()
    session.pop('email',None)
    session.pop('name',None)
    session.pop('role',None)
    session.pop('username',None)
    session.pop('id',None)
    # session.pop('loginmsg',None)

    return redirect(url_for("users.login"))


# account (update UserForm)
@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    userinfo = User.query.filter_by(email=session["email"]).first_or_404()

    form = UpdateUserForm()

    if request.method == 'POST':

        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.name = form.name.data
        current_user.number = form.number.data
        current_user.location = form.location.data
        current_user.pref_help = form.pref_help.data
        current_user.pref_therapistgender = form.pref_gender.data
        current_user.pref_medium = form.pref_medium.data
        

        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('userportal.uprofile'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('userportal/profile.html', profile_image=profile_image, form=form,userinfo=userinfo)



