from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/monitoreo.db'
db = SQLAlchemy(app)


class Monitoreo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpu = db.Column(db.String(10), nullable=True)
    memory = db.Column(db.String(10), nullable=False)
    disk = db.Column(db.String(10), nullable=False)
    httpd = db.Column(db.String(20), nullable=False)
