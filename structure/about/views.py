from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from structure import db
from structure.models import WebFeature,About
from structure.about.forms import UpdateAboutForm,AboutForm
from structure.about.picturehandler import update_about_pic

abouts = Blueprint('abouts',__name__)

@abouts.route('/create_about',methods=['GET','POST'])
@login_required
def create_about():
    form =  AboutForm()

    if form.validate_on_submit():

        about = About(title=form.title.data,
                             atext=form.text.data,
                             user_id=current_user.id,
                             location=form.location.data,
                             number= form.number.data,
                                email=form.email.data,
                                contact_subtitle=form.contact_subtitle.data,
                                about_subtitle=form.about_subtitle.data,
                                faq_title=form.faq_title.data,
                                faq_subtitle=form.faq_subtitle.data,
                                faq_paragraph=form.faq_paragraph.data,
                                testimonial_title=form.testimonial_title.data,
                                testimonial_subtitle=form.testimonial_subtitle.data,
                                testimonial_paragraph=form.testimonial_paragraph.data,
                                team_title=form.team_title.data,
                                team_subtitle=form.team_subtitle.data,
                                team_paragraph=form.team_paragraph.data,
                             )
        db.session.add(about)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_about.html',form=form)


# int: makes sure that the about_id gets passed as in integer
# instead of a string so we can look it up later.


# @abouts.route("/<int:about_id>/update", methods=['GET', 'POST'])
# @login_required
# def update(about_id):
#     about = About.query.get_or_404(about_id)
#     if about.author != current_user:
#         # Forbidden, No Access
#         abort(403)

#     form = BlogPostForm()
#     if form.validate_on_submit():
#         about.title = form.title.data
#         about.text = form.text.data
#         db.session.commit()
#         flash('About Updated')
#         return redirect(url_for('abouts.about', about_id=about.id))
#     # Pass back the old blog post information so they can start again with
#     # the old text and title.
#     elif request.method == 'GET':
#         form.title.data = about.title
#         form.text.data = about.text
#     return render_template('create_about.html', title='Update',
#                            form=form)





@abouts.route("/updateabout/<int:about_id>", methods=['GET', 'POST'])
@login_required
def updateabout(about_id):

    form = UpdateAboutForm()
    about = About.query.get_or_404(about_id)

    if request.method == 'POST':

        
        about.title = form.title.data
        about.subtitle = form.subtitle.data
        about.text = form.text.data
        about.location = form.location.data
        about.number = form.number.data
        about.email = form.email.data
        about.contact_subtitle = form.contact_subtitle.data
        about.about_subtitle = form.about_subtitle.data
        about.feature_subtitle = form.feature_subtitle.data
        about.feature_paragraph = form.feature_paragraph.data
        about.faq_title = form.faq_title.data
        about.faq_subtitle = form.faq_subtitle.data
        about.faq_paragraph = form.faq_paragraph.data
        about.testimonial_title = form.testimonial_title.data
        about.testimonial_subtitle = form.testimonial_subtitle.data
        about.testimonial_paragraph = form.testimonial_paragraph.data
        about.team_title = form.team_title.data
        about.team_paragraph = form.team_paragraph.data
        about.team_subtitle = form.team_subtitle.data
        about.logo = form.link3.data
        about.about_image = form.aboutimagelink.data
        about.carousel_image_1 = form.carousellink.data
        db.session.commit()
        print('updated')
        return redirect(request.args.get('next') or request.referrer )


    elif request.method == 'GET':
        form.title.data = about.title
        form.text.data = about.atext
        form.about_picture.data = about.image
        form.location.data = about.location
        form.number.data = about.number
        form.email.data = about.email
        form.contact_subtitle.data = about.contact_subtitle
        form.about_subtitle.data = about.about_subtitle
        form.feature_subtitle.data = about.feature_subtitle
        form.feature_paragraph.data = about.feature_paragraph
        form.subtitle.data = about.subtitle
        form.faq_title.data = about.faq_title
        form.faq_subtitle.data = about.faq_subtitle
        form.faq_paragraph.data = about.faq_paragraph
        form.testimonial_title.data = about.testimonial_title
        form.testimonial_subtitle.data = about.testimonial_subtitle
        form.testimonial_paragraph.data = about.testimonial_paragraph
        form.team_title.data = about.team_title
        form.team_subtitle.data = about.team_subtitle
        form.team_paragraph.data = about.team_paragraph
        form.link3.data = about.logo
        form.carousel_image_1.data = about.carousel_image_1



    return render_template('create_about.html', form=form,about=about)







@abouts.route("/updateasubntext/<int:about_id>", methods=['GET', 'POST'])
@login_required
def updateasubntext(about_id):

    form = UpdateAboutForm()
    about = About.query.get_or_404(about_id)

    if request.method == 'POST':
        about.about_subtitle = form.about_subtitle.data
        about.atext = form.text.data
        about.about_image = form.aboutimagelink.data

        flash(form.aboutimagelink.data)
        db.session.commit()
        print('updated')
        return redirect(request.args.get('next') or request.referrer )


    elif request.method == 'GET':
       
        form.text.data = about.atext
        form.about_subtitle.data = about.about_subtitle
        form.aboutimagelink.data = about.about_image
     

    return render_template('create_about.html', form=form,about=about)


@abouts.route("/updatefaqinfo/<int:about_id>", methods=['GET', 'POST'])
@login_required
def updatefaqinfo(about_id):

    form = UpdateAboutForm()
    about = About.query.get_or_404(about_id)

    if request.method == 'POST':
        about.team_title = form.team_title.data
        about.team_paragraph = form.team_paragraph.data
        about.team_subtitle = form.team_subtitle.data
        db.session.commit()
        print('updated')
        return redirect(request.args.get('next') or request.referrer )


    elif request.method == 'GET':
       
        form.faq_title.data = about.faq_title
        form.faq_subtitle.data = about.faq_subtitle
        form.faq_paragraph.data = about.faq_paragraph
     

    return render_template('create_about.html', form=form,about=about)



@abouts.route("/updatetestimonialsinfo/<int:about_id>", methods=['GET', 'POST'])
@login_required
def updatetestimonialsinfo(about_id):

    form = UpdateAboutForm()
    about = About.query.get_or_404(about_id)

    if request.method == 'POST':
        about.testimonial_title = form.testimonial_title.data
        about.testimonial_subtitle = form.testimonial_subtitle.data
        about.testimonial_paragraph = form.testimonial_paragraph.data
        db.session.commit()
        print('updated')
        return redirect(request.args.get('next') or request.referrer )


    elif request.method == 'GET':
       
        form.testimonial_title.data = about.testimonial_title
        form.testimonial_subtitle.data = about.testimonial_subtitle
        form.testimonial_paragraph.data = about.testimonial_paragraph
     

    return render_template('create_about.html', form=form,about=about)




@abouts.route("/updateteaminfo/<int:about_id>", methods=['GET', 'POST'])
@login_required
def updateteaminfo(about_id):

    form = UpdateAboutForm()
    about = About.query.get_or_404(about_id)

    if request.method == 'POST':
        about.team_title = form.team_title.data
        about.team_paragraph = form.team_paragraph.data
        about.team_subtitle = form.team_subtitle.data
        db.session.commit()
        print('updated')
        return redirect(request.args.get('next') or request.referrer )


    elif request.method == 'GET':
       
        form.team_title.data = about.team_title
        form.team_subtitle.data = about.team_subtitle
        form.team_paragraph.data = about.team_paragraph
     

    return render_template('create_about.html', form=form,about=about) 



@abouts.route("/updatefeatureinfo/<int:about_id>", methods=['GET', 'POST'])
@login_required
def updatefeatureinfo(about_id):

    form = UpdateAboutForm()
    about = About.query.get_or_404(about_id)

    if request.method == 'POST':
        about.feature_subtitle = form.feature_subtitle.data
        about.feature_paragraph = form.feature_paragraph.data
        db.session.commit()
        print('updated')
        return redirect(request.args.get('next') or request.referrer )


    elif request.method == 'GET':
       
        form.feature_subtitle.data = about.feature_subtitle
        form.feature_paragraph.data = about.feature_paragraph
     

    return render_template('create_about.html', form=form,about=about)



@abouts.route("/updatecarouselinfo/<int:about_id>", methods=['GET', 'POST'])
@login_required
def updatecarouselinfo(about_id):

    form = UpdateAboutForm()
    about = About.query.get_or_404(about_id)

    if request.method == 'POST':
        about.title = form.title.data
        about.subtitle = form.subtitle.data
        about.carousel_image_1 = form.carousellink.data
        db.session.commit()
        print('updated')
        return redirect(request.args.get('next') or request.referrer )


    elif request.method == 'GET':
       
        form.title.data = about.title
        form.subtitle.data = about.subtitle
     

    return render_template('create_about.html', form=form,about=about)





@abouts.route("/updatelna/<int:about_id>", methods=['GET', 'POST'])
@login_required
def updatelna(about_id):

    form = UpdateAboutForm()
    about = About.query.get_or_404(about_id)

    if request.method == 'POST':
        about.location = form.location.data
        about.number = form.number.data
        about.email = form.email.data
        about.contact_subtitle = form.contact_subtitle.data

        db.session.commit()
        print('updated')

        return redirect(request.args.get('next') or request.referrer )


    elif request.method == 'GET':
       
        form.location.data = about.location
        form.number.data = about.number
        form.email.data = about.email
        form.contact_subtitle.data = about.contact_subtitle

     

    return render_template('create_about.html', form=form,about=about)