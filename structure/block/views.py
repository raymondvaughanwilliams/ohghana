from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from structure import db
from structure.models import WebFeature,Block
from structure.block.forms import BlockForm

blocks = Blueprint('blocks',__name__)

@blocks.route('/create_block',methods=['GET','POST'])
@login_required
def create_block():
    form = BlockForm()

    if request.method == 'POST':

        block = Block(name=form.name.data,
                             status=form.status.data,
                                block_type="na"
                                                          )
        db.session.add(block)
        db.session.commit()
        flash("block Created")
        return redirect(request.args.get('next') or request.referrer )

    return render_template('create_block.html',form=form)


# # int: makes sure that the block_id gets passed as in integer
# # instead of a string so we can look it up later.
@blocks.route('/<int:block_id>')
def block(block_id):
    # grab the requested blog post by id number or return 404
    block = Block.query.get_or_404(block_id)
    return render_template('create_block.html',question=block.question,answer=block.answer
                            ,block=block
    )

@blocks.route("/update_block/<int:block_id>", methods=['GET', 'POST'])
@login_required
def update_block(block_id):
    block = Block.query.get_or_404(block_id)

    form = BlockForm()
    if request.method =='POST':
        block.name = form.name.data
        block.status = form.status.data
        db.session.commit()
        flash('Post Updated')
        return redirect(request.args.get('next') or request.referrer)
    # Pass back the old blog post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.question.data = block.question
        form.answer.data = block.answer
    return render_template('create_block.html',
                           form=form,block=block)





@blocks.route("/blocks", methods=['GET', 'POST'])
@login_required
def allblocks():

    block = Block.query.all()

    if block:
        question = block.question
        answer = block.answer
        return render_template('base2.html', question=question, answer=answer,block=block)

   
@blocks.route("/<int:block_id>/delete_block", methods=['POST','GET'])
@login_required
def delete_block(block_id):
    block = Block.query.get_or_404(block_id)
    db.session.delete(block)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
