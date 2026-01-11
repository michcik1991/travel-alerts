from flask import Blueprint, render_template, request
from app.services.search_service import SearchService

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        country = request.form["country"]
        results = SearchService().search(country)

    return render_template("index.html", results=results)