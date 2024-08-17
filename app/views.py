from flask import Blueprint, render_template
from . import databaseManagement as db

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    results = db.filter()
    return render_template("index.html", organizations=results)
