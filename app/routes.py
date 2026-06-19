from flask import Blueprint, request, render_template, jsonify

from app.services.wkt import read_point_wkt
from app.services.orthodromy import build_orthodromy, coordinates_to_wkt
from app.services.crs import transform_point_to_wgs84, transform_coordinates_from_wgs84
from app.services.forbidden_zones import find_forbidden_zone_intersections,geometries_to_wkt


main = Blueprint("main", __name__)

def parse_int(value: str, parameter_name: str):
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{parameter_name} must be integer")

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
    forbidden_zones = request.args.get("forbidden_zones")

    if not point1:
        return "Error: point1 parameter is required", 400

    if not point2:
        return "Error: point2 parameter is required", 400

    if not count:
        return "Error: count parameter is required", 400

    try:
        start_x, start_y = read_point_wkt(point1)
        end_x, end_y = read_point_wkt(point2)

        cs = parse_int(cs, "cs")
        count = parse_int(count, "count")

        start_lon, start_lat = transform_point_to_wgs84(start_x, start_y, cs)
        end_lon, end_lat = transform_point_to_wgs84(end_x, end_y, cs)

        coordinates_wgs84 = build_orthodromy(
            start_lon,
            start_lat,
            end_lon,
            end_lat,
            count
        )

        intersections = find_forbidden_zone_intersections(
            coordinates_wgs84,
            forbidden_zones
        )

        if intersections:
            intersections_wkt = geometries_to_wkt(intersections)
            map_wkt = coordinates_to_wkt(coordinates_wgs84)

            if response_format == "json":
                return jsonify({
                    "error": "Orthodromy intersects forbidden zone",
                    "map_wkt": map_wkt,
                    "intersections_wkt": intersections_wkt
                }), 400

            return "Error: Orthodromy intersects forbidden zone", 400

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