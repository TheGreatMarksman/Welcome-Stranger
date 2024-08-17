from flask import Blueprint, render_template
from . import databaseManagement as db

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    organizations = db.query_db("SELECT * FROM organizations")
    print(organizations)
    return render_template("index.html", organizations=organizations)