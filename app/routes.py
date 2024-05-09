from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('register.html', title='Register', form=form)