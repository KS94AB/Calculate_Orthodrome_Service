from shapely import wkt
from shapely.geometry import Point


def read_point_wkt(point_wkt: str):
    try:
        geometry = wkt.loads(point_wkt)
    except Exception:
        raise ValueError("Invalid WKT")

    if not isinstance(geometry, Point):
        raise ValueError("WKT must be POINT")

    lon = geometry.x
    lat = geometry.y

    return lon, lat