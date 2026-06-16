from shapely import wkt
from shapely.geometry import Point


def read_point_wkt(point_wkt: str):
    if not point_wkt or not point_wkt.strip():
        raise ValueError("WKT is required")
    try:
        geometry = wkt.loads(point_wkt)
    except Exception:
        raise ValueError("Invalid WKT")
    
    if geometry.is_empty:
        raise ValueError("POINT must not be empty")

    if not isinstance(geometry, Point):
        raise ValueError("WKT must be POINT")
    

    lon = geometry.x
    lat = geometry.y

    return lon, lat