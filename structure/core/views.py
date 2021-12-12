from flask import render_template,request,Blueprint
from structure.models import User,About,Price, WebFeature,Faq,Testimonial,Team
# from structure.team.views import team

core = Blueprint('core',__name__)

@core.route('/')
def index():
    '''
    This is the home page view. Notice how it uses pagination to show a limited
    number of posts by limiting its query size and then calling paginate.
    '''
    page = request.args.get('page', 1, type=int)
    about = About.query.all()
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
    return render_template('base.html',about= about)

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

    page = request.args.get('page', 1, type=int)
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    about = About.query.get(1)
    price = Price.query.all()
    faq = Faq.query.all()
    testimonial = Testimonial.query.all()
    team= Team.query.all()
    serv = Price.features
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('base2.html',web_features=web_features, about=about,pricing=price,faq=faq,testimonial=testimonial,team=team)



@core.route('/editui')
def editui():
    '''
    Example view of any other "core" page. Such as a info page, about page,
    contact page. Any page that doesn't really sync with one of the models.
    '''

    page = request.args.get('page', 1, type=int)
    web_features = WebFeature.query.order_by(WebFeature.date.desc()).paginate(page=page, per_page=10)
    about = About.query.get(1)
    price = Price.query.all()
    faq = Faq.query.all()
    testimonial = Testimonial.query.all()
    team= Team.query.all()
    serv = Price.features
    # services=[]
    # service= serv.split(',')
    # services.append(service)
    return render_template('editui.html',web_features=web_features, about=about,pricing=price,faq=faq,testimonial=testimonial,team=team)
