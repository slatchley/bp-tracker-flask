from datetime import datetime
import io
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from matplotlib import pyplot as plt
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

@app.route("/delete/<int:reading_id>", methods=["POST"])
def delete(reading_id):
    r = Reading.query.get_or_404(reading_id)
    db.session.delete(r)
    db.session.commit()
    flash("Reading deleted.")
    return redirect(url_for("index"))

@app.route("/plot.png")
def plot_png():
    readings = Reading.query.order_by(Reading.created_at.asc()).all()

    fig, ax = plt.subplots(figsize=(8, 4.5))
    if readings:
        xs = [r.created_at for r in readings]
        sys_vals = [r.systolic for r in readings]
        dia_vals = [r.diastolic for r in readings]
        pulse_vals = [r.pulse for r in readings]

        ax.plot(xs, sys_vals, marker='o', label="Systolic")
        ax.plot(xs, dia_vals, marker='o', label="Diastolic")
        ax.plot(xs, pulse_vals, marker='o', label="Pulse")

        # after plotting your data but before ax.legend()
        ax.axhline(y=130, color="red", linestyle="--", linewidth=1, label="High Systolic (130)")
        ax.axhline(y=80, color="orange", linestyle="--", linewidth=1, label="High Diastolic (80)")


        # Get data ranges
        all_y = sys_vals + dia_vals + [p for p in pulse_vals if p is not None]
        ymin, ymax = min(all_y), max(all_y)

        # Apply padding and defaults
        ymin = min(ymin, 40)
        ymax = max(ymax, 200)
        print(ymin, ymax)
        ax.set_ylim(ymin, ymax)

      
        ax.set_title("Blood Pressure Over Time")
        ax.set_xlabel("Date/Time")
        ax.set_ylabel("mmHg / bpm")
        ax.grid(True, alpha=0.3)
        ax.legend()
        fig.autofmt_xdate()
    else:
        ax.text(0.5, 0.5, "No readings yet", ha='center', va='center', fontsize=20, color='gray')
        ax.set_xticks([])
        ax.set_yticks([])

    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")