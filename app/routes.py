from flask import render_template,redirect, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sabrina'}
    return render_template('index.html')

@app.route("/add", methods=["POST"])
def add():
    print("Add function called")
    return redirect(url_for("index"))


@app.route("/plot.png")
def plot_png():
    return("Plot function called")  # Placeholder for actual plot generation logic