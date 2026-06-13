from flask import Blueprint, request, jsonify

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "Calculate service is running"

@main.route("/orthodromy")
def orthodromy():
    return " "
