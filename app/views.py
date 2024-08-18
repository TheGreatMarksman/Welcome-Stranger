from flask import Blueprint, render_template, request, jsonify
from . import databaseManagement as db

blueprint = Blueprint("views", __name__)

@blueprint.route("/")
def home():
    provinces = db.get_provinces()
    cities = db.get_cities()
    return render_template("index.html", provinces=provinces, cities=cities)

@blueprint.route('/filter', methods=['POST'])
def filter():
    filters = request.json
    province = filters.get('province')
    city = filters.get('city')
    nation = filters.get('nation')
    language = filters.get('language')
    has_service = filters.get('has_service')

    # Pass the filters to the function
    charities = filter_locations(
        province=province,
        cities=[city] if city else None,
        nations=[nation] if nation else None,
        languages=[language] if language else None,
        has_church_service= 1 if has_service else None
    )

    # Return the filtered results as JSON
    return jsonify(charities)

def filter_locations(province=None, cities=None, nations=None, languages=None, has_church_service=None):
    print(has_church_service)
    results = db.filter(province, cities, languages, nations, has_church_service)
    return [db.rowToDictionary(row) for row in results]