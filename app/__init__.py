from flask import Flask
from app import views
from . import databaseManagement as db

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views.blueprint)
    db.init_app(app)
    return app 