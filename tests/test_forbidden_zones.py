import json

from app.services.forbidden_zones import (
    parse_forbidden_zones,
    find_forbidden_zone_intersections
)

#запретная зона не нарисована 
def test_empty_zones():
    zones = parse_forbidden_zones("")

    assert zones == []

#запретная зона успешно парсится и превращается в полигон
def test_parse_polygon():
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [33, 56],
                            [37, 56],
                            [37, 58],
                            [33, 58],
                            [33, 56]
                        ]
                    ]
                }
            }
        ]
    }
    zones = parse_forbidden_zones(json.dumps(data))
    assert len(zones) == 1
    assert zones[0].geom_type == "Polygon"

#линия пересекает полигон и find_forbidden_zone_intersections находит это пересечение
def test_line_intersects_zone():
    line = [
        (30, 55),
        (34, 57),
        (40, 60)
    ]
    data = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [33, 56],
                            [37, 56],
                            [37, 58],
                            [33, 58],
                            [33, 56]
                        ]
                    ]
                }
            }
        ]
    }
    intersections = find_forbidden_zone_intersections(
        line,
        json.dumps(data)
    )
    assert len(intersections) > 0