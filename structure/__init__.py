import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from sqlalchemy import MetaData
from flask_mail import Mail, Message
from flask_mail import Mail, Message
from dotenv import load_dotenv
from flask_apscheduler import APScheduler
from flask_uploads import UploadSet, configure_uploads, IMAGES


app = Flask(__name__)
load_dotenv()


scheduler = APScheduler()

app.config['SECRET_KEY'] = 'asecretkey'
############################
### DATABASE SETUP ##########
########################
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(app,metadata=MetaData(naming_convention=naming_convention))

Migrate(app,db)
migrate = Migrate(app, db, render_as_batch=True)
with app.app_context():
    if db.engine.url.drivername == "sqlite":
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db, render_as_batch=True)









app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images/certificates')
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
# patch_request_class(app)


app.config.update(
    UPLOAD_PATH = os.path.join(basedir, 'static')
)

#########################
#########################
# LOGIN CONFIGS
login_manager = LoginManager()


login_manager.init_app(app)
login_manager.login_view = 'users.login'




app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "raymondvaughanwilliams@gmail.com"
app.config["MAIL_PASSWORD"] = os.environ.get('MAIL_PASSWORD')

mail = Mail(app)
# emailpassword = os.environ.get('MAIL_PASSWORD')

from structure.core.views import core
from structure.users.views import users
from structure.web_features.views import web_features
from structure.error_pages.handlers import error_pages
from structure.about.views import abouts
from structure.pricing.views import pricings 
from structure.faq.views import faqs
from structure.testimonial.views import testimonials
from structure.team.views import teams
from structure.block.views import blocks
from structure.appearance.views import appearances
from structure.web.views import web
from structure.userportal.views import userportal
from structure.therapistportal.views import therapistportal

app.register_blueprint(core)
app.register_blueprint(users)
app.register_blueprint(web_features)
app.register_blueprint(error_pages)
app.register_blueprint(abouts)
app.register_blueprint(pricings)
app.register_blueprint(faqs)
app.register_blueprint(testimonials)
app.register_blueprint(teams)
app.register_blueprint(blocks)
app.register_blueprint(appearances)
app.register_blueprint(web)
app.register_blueprint(userportal)
app.register_blueprint(therapistportal)



