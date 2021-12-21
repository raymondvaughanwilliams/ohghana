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
def create_team():

    
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
        return redirect(request.args.get('next') or request.referrer )

   


    return render_template('create_team.html', team_picture=team_picture, form=form)



@teams.route("/update_team/<int:team_id>", methods=['GET', 'POST'])
@login_required
def update_team(team_id):
    team = Team.query.get_or_404(team_id)


    form = TeamForm()
    if request.method=='POST':

        team.name = form.name.data
        team.position = form.position.data
        team.faceboook = form.facebook.data
        team.instagram = form.instagram.data
        team.twitter = form.twitter.data
        team.picture = form.link.data

        db.session.commit()
        flash('Post Updated')
        return redirect(request.args.get('next') or request.referrer )
   
    elif request.method == 'GET':
        form.name.data = team.name
        form.position.data = team.position
        form.instagram.data = team.instagram
        form.twitter.data = team.twitter
        form.picture.data = team.picture
        form.facebook.data = team.faceboook
    return render_template('update_team.html',
                           form=form,team=team)




@teams.route("/delete_post/<int:team_id>", methods=['POST','GET'])
@login_required
def delete_post(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
