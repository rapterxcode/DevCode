from flask import Flask
from werkzeug.security import generate_password_hash
from database import db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from models import *
from routes import register_routes

register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)