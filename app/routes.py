from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from app import app, db
from app.models import Reading


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Sabrina'}
    now = datetime.now().strftime('%Y-%m-%d')
    sort = request.args.get("sort", "created_at_desc")
    q = Reading.query
    
    return render_template('index.html',now=now, user=user, readings=q, sort=sort)

@app.route("/add", methods=["POST"])
def add():
    try:
        systolic = int(request.form["systolic"])
        diastolic = int(request.form["diastolic"])
        pulse_raw = request.form.get("pulse", "").strip()
        pulse = int(pulse_raw) if pulse_raw else None
        date_str = request.form.get("date")
        if date_str:
            # Use only date, set time to now
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            created_at = datetime.combine(date_obj.date(), datetime.now().time())
        else:
            created_at = datetime.now()
    except (ValueError, KeyError):
        flash("Please enter valid integers for systolic/diastolic and optional pulse.")
        return redirect(url_for("index"))

    if not (40 <= diastolic <= 150 and 70 <= systolic <= 260):
        flash("Out-of-range value. Check systolic/diastolic entries.")
        return redirect(url_for("index"))

    if pulse is not None and not (20 <= pulse <= 220):
        flash("Pulse out of range.")
        return redirect(url_for("index"))

    reading = Reading(systolic=systolic, diastolic=diastolic, pulse=pulse, created_at=created_at)
    print(reading)
    db.session.add(reading)
    db.session.commit()
    flash("Reading added.")
    return redirect(url_for("index"))


@app.route("/plot.png")
def plot_png():
    return("Plot function called")  # Placeholder for actual plot generation logic