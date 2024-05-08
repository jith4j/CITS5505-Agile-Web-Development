from flask import render_template, flash, redirect, url_for
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/profile")
def profile():
    return render_template('profile.html')