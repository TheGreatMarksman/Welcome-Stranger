from flask import Blueprint, render_template
from . import databaseManagement as db

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    results = db.filter()
    results = [db.rowToDictionary(row) for row in results]
    return render_template("index.html", charities=results)
