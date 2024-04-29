from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/")
def landing_page():
    return render_template('index.html')

@main.route("/success")
def success():
    return render_template('success.html')

@main.route("/profile")
def profile():
    return render_template('profile.html')