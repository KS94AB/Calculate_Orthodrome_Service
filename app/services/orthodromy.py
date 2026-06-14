from pyproj import Geod


geod = Geod(ellps="WGS84")


def build_orthodromy(
    start_lon: float,
    start_lat: float,
    end_lon: float,
    end_lat: float,
    nodes_count: int
):
    if nodes_count < 2:
        raise ValueError("nodes_count must be at least 2")

    intermediate_count = nodes_count - 2

    if intermediate_count > 0:
        intermediate_points = geod.npts(
            start_lon,
            start_lat,
            end_lon,
            end_lat,
            intermediate_count
        )
    else:
        intermediate_points = []

    coordinates = [(start_lon, start_lat)]
    coordinates.extend(intermediate_points)
    coordinates.append((end_lon, end_lat))

    return coordinates



def format_number(value: float) -> str:
    value = round(value, 6)

    if value == -0.0:
        value = 0.0

    text = f"{value:.6f}"
    text = text.rstrip("0").rstrip(".")

    return text




def coordinates_to_wkt(coordinates):
    points_text = []

    for lon, lat in coordinates:
        point_text = f"{format_number(lon)} {format_number(lat)}"
        points_text.append(point_text)

    return f"LINESTRING({', '.join(points_text)})"
