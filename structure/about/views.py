from PIL import Image
import requests
from io import BytesIO
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template,url_for,flash,redirect,request,Blueprint,session
from werkzeug.utils import secure_filename
from structure import db,mail ,photos
import secrets
from structure.about.forms import AboutForm


about = Blueprint('about',__name__)


    

# # Save menu items to the database
# for menu_item in menu_items:
#     db.session.add(menu_item)

# db.session.commit()
