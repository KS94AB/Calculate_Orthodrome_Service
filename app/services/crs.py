from pyproj import Transformer


SUPPORTED_CRS = {4326, 4284, 3857}


def validate_crs(crs: int):
    if crs not in SUPPORTED_CRS:
        raise ValueError("CRS must be 4326, 4284 or 3857")


def transform_point_to_wgs84(x: float, y: float, source_crs: int):
    validate_crs(source_crs)

    if source_crs == 4326:
        return x, y

    transformer = Transformer.from_crs(
        f"EPSG:{source_crs}",
        "EPSG:4326",
        always_xy=True
    )

    lon, lat = transformer.transform(x, y)

    return lon, lat


def transform_point_from_wgs84(lon: float, lat: float, target_crs: int):
    validate_crs(target_crs)

    if target_crs == 4326:
        return lon, lat

    transformer = Transformer.from_crs(
        "EPSG:4326",
        f"EPSG:{target_crs}",
        always_xy=True
    )

    x, y = transformer.transform(lon, lat)

    return x, y


def transform_coordinates_from_wgs84(coordinates, target_crs: int):
    result = []

    for lon, lat in coordinates:
        x, y = transform_point_from_wgs84(lon, lat, target_crs)
        result.append((x, y))

    return result