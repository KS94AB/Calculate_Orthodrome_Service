from flask import Blueprint, request, jsonify

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return "Calculate service is running"

@main.route("/orthodromy")
def orthodromy():
    start_lon = request.args.get("start_lon")
    start_lat = request.args.get("start_lat")
    end_lon = request.args.get("end_lon")
    end_lat = request.args.get("end_lat")
    nodes_count = request.args.get("nodes_count")

    return jsonify({
        "start_lon" : start_lon,
        "start_lat" : start_lat,
        "end_lon" : end_lon,
        "end_lat" : end_lat,
        "nodes_count" : nodes_count
    })