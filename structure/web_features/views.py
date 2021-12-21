from flask import render_template,url_for,flash, redirect,request,Blueprint,abort
from flask_login import current_user,login_required
from structure import db
from structure.models import WebFeature
from structure.web_features.forms import WebFeatureForm

web_features = Blueprint('web_features',__name__)

@web_features.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = WebFeatureForm()

    if request.method == 'POST':

        web_feature = WebFeature(title=form.title.data,
                             wtext=form.text.data,

                             )
        db.session.add(web_feature)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(request.args.get('next') or request.referrer )


    return render_template('create_post.html',form=form)


# int: makes sure that the web_feature_id gets passed as in integer
# instead of a string so we can look it up later.
@web_features.route('/<int:web_feature_id>')
def web_feature(web_feature_id):
    # grab the requested blog post by id number or return 404
    web_feature = WebFeature.query.get_or_404(web_feature_id)
    return render_template('web_feature.html',title=web_feature.title,
                            date=web_feature.date,web_feature=web_feature
    )

@web_features.route("/<int:web_feature_id>/update", methods=['GET', 'POST'])
@login_required
def update(web_feature_id):
    web_feature = WebFeature.query.get_or_404(web_feature_id)


    form = WebFeatureForm()
    if request.method =='POST':
        web_feature.title = form.title.data
        web_feature.wtext = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(request.args.get('next') or request.referrer )

    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = web_feature.title
        form.text.data = web_feature.wtext
    return render_template('update_features.html', title='Update',
                           form=form,web_feature=web_feature)


@web_features.route("/<int:web_feature_id>/delete", methods=['POST','GET'])
@login_required
def delete_post(web_feature_id):
    web_feature = WebFeature.query.get_or_404(web_feature_id)
    db.session.delete(web_feature)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
