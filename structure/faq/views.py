from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from structure import db
from structure.models import Faq
from structure.faq.forms import FaqForm

faqs = Blueprint('faqs',__name__)

@faqs.route('/create_faq',methods=['GET','POST'])
@login_required
def create_faq():
    form = FaqForm()

    if request.method == 'POST':

        faq = Faq(question=form.question.data,
                             answer=form.answer.data,
                             )
        db.session.add(faq)
        db.session.commit()
        flash("Faq Created")
        return redirect(request.args.get('next') or request.referrer )

    return render_template('create_faq.html')


# # int: makes sure that the faq_id gets passed as in integer
# # instead of a string so we can look it up later.
@faqs.route('/<int:faq_id>')
def faq(faq_id):
    # grab the requested blog post by id number or return 404
    faq = Faq.query.get_or_404(faq_id)
    return render_template('create_faq.html',question=faq.question,answer=faq.answer
                            ,faq=faq
    )

@faqs.route("/update/<int:faq_id>", methods=['GET', 'POST'])
@login_required
def updatefaq(faq_id):
    faq = Faq.query.get_or_404(faq_id)

    form = FaqForm()
    if request.method =='POST':
        faq.question = form.question.data
        faq.answer = form.answer.data
        db.session.commit()
        flash('Post Updated')
        return redirect(request.args.get('next') or request.referrer)
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.question.data = faq.question
        form.answer.data = faq.answer
    return render_template('create_faq.html',
                           form=form,faq=faq)





@faqs.route("/faqs", methods=['GET', 'POST'])
@login_required
def allfaqs():

    faq = Faq.query.all()

    if faq:
        question = faq.question
        answer = faq.answer
        return render_template('base2.html', question=question, answer=answer,faq=faq)

   
@faqs.route("/<int:faq_id>/delete_faq", methods=['POST','GET'])
@login_required
def delete_faq(faq_id):
    faq = Faq.query.get_or_404(faq_id)
    db.session.delete(faq)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
