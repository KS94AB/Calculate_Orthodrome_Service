from flask import Blueprint, request, render_template, jsonify

from app.services.wkt import read_point_wkt
from app.services.orthodromy import build_orthodromy, coordinates_to_wkt
from app.services.crs import transform_point_to_wgs84, transform_coordinates_from_wgs84


main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/orthodromy")
def orthodromy():
    point1 = request.args.get("point1")
    point2 = request.args.get("point2")
    cs = request.args.get("cs", "4326")
    count = request.args.get("count")
    response_format = request.args.get("format")

    if not point1:
        return "Error: point1 parameter is required", 400

    if not point2:
        return "Error: point2 parameter is required", 400

    if not count:
        return "Error: count parameter is required", 400

    try:
        start_x, start_y = read_point_wkt(point1)
        end_x, end_y = read_point_wkt(point2)

        cs = int(cs)
        count = int(count)

        start_lon, start_lat = transform_point_to_wgs84(start_x, start_y, cs)
        end_lon, end_lat = transform_point_to_wgs84(end_x, end_y, cs)

        coordinates_wgs84 = build_orthodromy(
            start_lon,
            start_lat,
            end_lon,
            end_lat,
            count
        )

        result_coordinates = transform_coordinates_from_wgs84(
            coordinates_wgs84,
            cs
        )

        line_wkt = coordinates_to_wkt(result_coordinates)
        map_wkt = coordinates_to_wkt(coordinates_wgs84)

    except ValueError as error:
        return f"Error: {error}", 400

    if response_format == "json":
        return jsonify({
            "wkt": line_wkt,
            "map_wkt": map_wkt,
            "cs": cs,
            "count": count
        })

    return line_wkt