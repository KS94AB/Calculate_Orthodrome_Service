import json

from shapely.geometry import LineString, shape


def parse_forbidden_zones(forbidden_zones_text: str):
    if not forbidden_zones_text:
        return []

    try:
        data = json.loads(forbidden_zones_text)
    except json.JSONDecodeError:
        raise ValueError("Invalid forbidden_zones JSON")

    if data.get("type") != "FeatureCollection":
        raise ValueError("forbidden_zones must be GeoJSON FeatureCollection")

    zones = []

    for feature in data.get("features", []):
        geometry_data = feature.get("geometry")

        if geometry_data is None:
            continue

        geometry = shape(geometry_data)

        if geometry.is_empty:
            continue

        if geometry.geom_type not in ("Polygon", "MultiPolygon"):
            raise ValueError("Forbidden zones must be Polygon or MultiPolygon")

        zones.append(geometry)

    return zones


def find_forbidden_zone_intersections(coordinates_wgs84, forbidden_zones_text: str):
    zones = parse_forbidden_zones(forbidden_zones_text)

    if not zones:
        return []

    orthodromy_line = LineString(coordinates_wgs84)
    intersections = []

    for zone in zones:
        if orthodromy_line.intersects(zone):
            intersection = orthodromy_line.intersection(zone)

            if not intersection.is_empty:
                intersections.append(intersection)

    return intersections


def geometries_to_wkt(geometries):
    result = []

    for geometry in geometries:
        result.append(geometry.wkt)

    return result