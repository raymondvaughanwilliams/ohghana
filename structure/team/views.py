from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from structure import db,app
import os
from structure.models import WebFeature,About,Team
from structure.team.forms import UpdateTeamForm,TeamForm
from structure.team.picture_handler import team_picture


teams = Blueprint('teams',__name__)


#NK

@teams.route("/create_team", methods=['GET', 'POST'])
@login_required
def team():

    
    form = TeamForm()
    team= Team.query.all()

    if form.validate_on_submit():
        
    

        team = Team(name=form.name.data,
                    position=form.position.data,
                    faceboook=form.facebook.data,
                    instagram=form.instagram.data,
                    twitter=form.twitter.data,
                    picture=form.link.data,)



        db.session.add(team)
        db.session.commit()
        flash('Done')
        return redirect(url_for('core.index'))

   


    return render_template('create_team.html', team_picture=team_picture, form=form)










# @teams.route("/create_team", methods=['GET', 'POST'])
# @login_required
# def team():

    
#     form = TeamForm()
#     team= Team.query.all()

#     if form.validate_on_submit():

#         if form.picture.data:
#             pic = team_picture(form.picture.data)
#             team.picture = pic

#         team.name = form.name.data
#         team.position = form.position.data
#         team.facebook = form.facebook.data
#         team.twitter = form.twitter.data
#         team.instagram = form.instagram.data
#         db.session.commit()
#         flash('Done')
#         return redirect(url_for('teams.create_team'))

#     # elif request.method == 'GET':
#     #     form.name.data = team.name
#     #     form.position.data = team.position
#     #     form.facebook.data = team.facebook
#     #     form.twitter.data = team.twitter
#     #     form.instagram.data = team.instagram



#     team_picture = url_for('static', filename='profile_pics/' + str(storage_filename))
#     return render_template('create_team.html', team_picture=team_picture, form=form)



# @teams.route('/create_tea', methods=['POST'])
# def create_tea():
#     form = TeamForm()
#     if form.validate_on_submit():

#         pic = form.picture.data
#         if not pic:
#             return 'No pic uploaded!', 400

#         filename = secure_filename(pic.filename)
#         mimetype = filename.split('.')[-1]
#     # mimetype = pic.mimetype
#         if not filename or not mimetype:
#             return 'Bad upload!', 400

#         team = Team(picture=pic.read(), name=form.name.data, position=form.position.data,faceboook=form.facebook.data,twitter=form.twitter.data,instagram=form.instagram.data, mimetype=mimetype)
#         db.session.add(team)
#         db.session.commit()

#         return render_template('create_team.html', team=team,form=form)



# if form.picture.data:
#             form_picture = form.picture.data
#             random_hex = secrets.token_hex(8)
#             _, f_ext = os.path.splitext(form_picture.filename)
#             print(form_picture.filename)
#             picture_fn = random_hex + f_ext