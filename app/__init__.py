from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
os.environ["MPLBACKEND"] = "Agg"
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bp_readings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'change-me'  # needed for flash messages
db = SQLAlchemy(app)



from app import routes, models