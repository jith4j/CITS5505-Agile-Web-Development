from flask import render_template, flash, redirect, url_for, request, jsonify
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Question, Answer, Reply, Like
import os
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import humanize

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/success")
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('forum', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('forum', username=user.username)
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/forgotPassword', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Generate a random 6-digit OTP
    otp = ''.join(random.choices(string.digits, k=6))

    # Set up the MIME message
    message = MIMEMultipart()
    message['From'] = os.getenv('SENDGRID_SENDER_EMAIL')
    message['To'] = email
    message['Subject'] = 'Your OTP for Password Reset'
    message.attach(MIMEText(f"<strong>Your OTP is: {otp}</strong>", 'html'))

    try:
        with smtplib.SMTP('smtp.sendgrid.net', 587) as server:
            server.starttls()  # Secure the connection
            server.login('apikey', os.getenv('SENDGRID_API_KEY'))
            server.send_message(message)
        return jsonify({'message': 'OTP sent successfully', 'otp': otp}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/forum/<username>', methods=['GET', 'POST'])
@login_required
def forum(username):
    if current_user.username != username:
        return "Unauthorized access", 403

    user = db.session.scalar(sa.select(User).where(User.username == username))
    if user is None:
        return "User not found", 404

    sort_order = request.args.get('sort', 'desc')

    if request.method == 'POST':
        question_text = request.form.get('question')
        if question_text:
            question = Question(question=question_text, author=current_user)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('forum', username=username))

    ques_list = []

    if sort_order == 'asc':
        query = sa.select(Question).order_by(Question.timestamp.asc())
    else:
        query = sa.select(Question).order_by(Question.timestamp.desc())

    ques = db.session.scalars(query).all()

    for q in ques:
        ques_list.append({
            'author': q.author.username,
            'author_avatar': q.author,
            'body': q.question,
            'timestamp': q.timestamp,
            'id': q.id
        })

    return render_template('forum.html', username=user.username, ques=ques_list, sort=sort_order, humanize=humanize)

@app.route('/answer/<qid>', methods=['GET', 'POST'])
@login_required
def answer(qid):
    ans_list = []
    ans = db.session.scalars(sa.select(Answer).where(Answer.question_id == qid)).all()
    ques = db.session.get(Question, qid)
    for a in ans:
        replies = db.session.scalars(sa.select(Reply).where(Reply.answer_id == a.id)).all()
        likes = db.session.scalars(sa.select(Like).where(Like.answer_id == a.id)).all()
        user_liked = any(like.user_id == current_user.id for like in likes)
        ans_list.append({
            'answer': a.answer,
            'id': a.id,
            'author': a.author.username,
            'author_avatar': a.author,
            'timestamp': a.timestamp,
            'all_replies': replies,
            'likes': len(likes),
            'user_liked': user_liked
        })
    return render_template('answer.html', ans=ans_list, question=ques)

@app.route('/latestAnswer/<qid>', methods=['GET', 'POST'])
@login_required
def latestAnswer(qid):
    ans_list=[]
    ans=db.session.scalar(sa.select(Answer).where(Answer.question_id==qid).order_by(Answer.timestamp.desc()))
    if ans:
        ans_list=[{'answer': ans.answer}]
    return jsonify(ans_list)

@app.route('/addAnswer/<qid>', methods=['GET', 'POST'])
@login_required
def add_answer(qid):
    question = db.session.get(Question, qid)
    if not question:
        return "Question not found", 404

    if request.method == 'POST':
        answer_text = request.form.get('answer')
        if answer_text:
            answer = Answer(answer=answer_text, author=current_user, question_id=qid)
            print(qid)
            db.session.add(answer)
            db.session.commit()
            flash('Your answer has been posted.')
            return redirect(url_for('answer', qid=qid))

    ans_list = db.session.scalars(sa.select(Answer).where(Answer.question_id == qid)).all()
    return render_template('answer.html', ans_list=ans_list, question=question)


@app.route("/profile")
@login_required
def profile():
    curruser = current_user
    ques_list = db.session.scalars(curruser.question_posts.select()).all()
    ans_list = db.session.scalars(curruser.answer_posts.select()).all()
    return render_template('profile.html', user=curruser, ques=ques_list, ans= ans_list)

@app.route('/addReply/<int:aid>', methods=['POST'])
@login_required
def add_reply(aid):
    reply_text = request.form.get('reply')
    if reply_text:
        answer = db.session.get(Answer, aid)
        if answer is not None:
            reply = Reply(reply=reply_text, author=current_user, answer_id=aid, question_id=answer.question_id)
            db.session.add(reply)
            db.session.commit()
            flash('Reply added!')
    return redirect(url_for('answer', qid=answer.question_id))


@app.route('/toggle_like/<int:aid>', methods=['POST'])
@login_required
def toggle_like(aid):
    answer = db.session.get(Answer, aid)
    if answer is None:
        flash('Answer not found.', 'danger')
        return jsonify({'error': 'Answer not found'}), 404

    like = db.session.scalar(sa.select(Like).where(Like.user_id == current_user.id, Like.answer_id == aid))
    if like is None:
        new_like = Like(user_id=current_user.id, answer_id=aid)
        db.session.add(new_like)
        liked = True
    else:
        db.session.delete(like)
        liked = False
    db.session.commit()

    likes_count = db.session.scalar(sa.select(sa.func.count(Like.id)).where(Like.answer_id == aid))
    return jsonify({'liked': liked, 'likes': likes_count})
