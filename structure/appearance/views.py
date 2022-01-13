from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from structure import db
from structure.models import WebFeature,Appearance
from structure.appearance.forms import AppearanceForm,AppearanceForm1

appearances = Blueprint('appearances',__name__)

@appearances.route('/create_appearance',methods=['GET','POST'])
@login_required
def create_appearance():
    form = AppearanceForm()

    if request.method == 'POST':

        appearance = Appearance(name=form.name.data,
                             status=form.status.data,
                                appearance_type="na"
                                                          )
        db.session.add(appearance)
        db.session.commit()
        flash("appearance Created")
        return redirect(request.args.get('next') or request.referrer )

    return render_template('create_appearance.html',form=form)


# # int: makes sure that the appearance_id gets passed as in integer
# # instead of a string so we can look it up later.
@appearances.route('/<int:appearance_id>')
def appearance(appearance_id):
    # grab the requested blog post by id number or return 404
    appearance = Appearance.query.get_or_404(appearance_id)
    return render_template('create_appearance.html',question=appearance.question,answer=appearance.answer
                            ,appearance=appearance
    )

@appearances.route("/update_appearance/<int:appearance_id>", methods=['GET', 'POST'])
@login_required
def update_appearance(appearance_id):
    appearance = Appearance.query.get_or_404(appearance_id)

    form = AppearanceForm(obj=appearance)

     
    if request.method =='POST':
        appearance.title_color = form.title_color.data
        appearance.subtitle_color = form.subtitle_color.data
        appearance.paragraph_color = form.paragraph_color.data
        appearance.title_font = form.title_font.data
        appearance.subtitle_font = form.subtitle_font.data
        appearance.paragraph_font = form.paragraph_font.data
        appearance.title_size = form.title_size.data
        appearance.subtitle_size = form.subtitle_size.data
        appearance.paragraph_size = form.paragraph_size.data
        appearance.bootstrap_class1 = form.bootstrap_class1.data
        appearance.bootstrap_class2 = form.bootstrap_class2.data
        appearance.bootstrap_class3 = form.bootstrap_class3.data


        db.session.commit()
        flash('Post Updated')
        return redirect(request.args.get('next') or request.referrer)
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title_color.data = appearance.title_color
        form.subtitle_color.data = appearance.subtitle_color
        form.paragraph_color.data = appearance.paragraph_color
        form.title_font.data = appearance.title_font
        form.subtitle_font.data = appearance.subtitle_font
        form.paragraph_font.data = appearance.paragraph_font
        form.title_size.data = appearance.title_size
        form.subtitle_size.data = appearance.subtitle_size
        form.paragraph_size.data = appearance.paragraph_size
        form.bootstrap_class1.data = appearance.bootstrap_class1
        form.bootstrap_class2.data = appearance.bootstrap_class2
        form.bootstrap_class3.data = appearance.bootstrap_class3


    return render_template('create_appearance.html',
                           form=form,appearance=appearance)





# @appearances.route("/appearances", methods=['GET', 'POST'])
# @login_required
# def allappearances():

#     appearance = Appearance.query.all()

#     if appearance:
#         question = appearance.question
#         answer = appearance.answer
#         return render_template('base2.html', question=question, answer=answer,appearance=appearance)

   
@appearances.route("/<int:appearance_id>/delete_appearance", methods=['POST','GET'])
@login_required
def delete_appearance(appearance_id):
    appearance = Appearance.query.get_or_404(appearance_id)
    db.session.delete(appearance)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
