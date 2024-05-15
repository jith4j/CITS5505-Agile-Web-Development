from flask import render_template, flash, redirect, url_for, request, jsonify
from urllib.parse import urlsplit
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Question, Answer
import os
import random
import string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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
    return render_template('login.html', title='Sign In', form=form)

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

    if request.method == 'POST':
        question_text = request.form.get('question')
        if question_text:
            question = Question(question=question_text, author=current_user)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('forum', username=username))

    ques_list = []
    query = sa.select(User)
    users = db.session.scalars(query).all()
    for u in users:
        qu = sa.select(Question).where(Question.author == u)
        ques = db.session.scalars(qu).all()
        for q in ques:
            ques_list.append({'author': u.username, 'body': q.question, 'timestamp': q.timestamp, 'id': q.id})

    return render_template('forum.html', username=user.username, ques=ques_list)

@app.route('/answer/<qid>', methods=['GET', 'POST'])
@login_required
def answer(qid):
    ans_list=[]
    ans=db.session.scalars(sa.select(Answer).where(Answer.question_id==qid)).all()
    ques = db.session.get(Question, qid)
    for a in ans:
        ans_list.append({'answer':a.answer})
    return render_template('answer.html', ans=ans_list, question=ques.question)

@app.route("/profile")
@login_required
def profile():
    curruser = current_user
    return render_template('profile.html', user=curruser)