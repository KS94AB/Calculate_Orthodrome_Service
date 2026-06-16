import pytest

from app.services.orthodromy import build_orthodromy, coordinates_to_wkt

#кол-во узлов
def test_build_orthodromy_returns_required_count():
    coordinates = build_orthodromy(30, 55, 40, 60, 5)

    assert len(coordinates) == 5

#первая точка остается начальной, последняя последней
def test_build_orthodromy_first_and_last_points():
    coordinates = build_orthodromy(30, 55, 40, 60, 5)

    assert coordinates[0] == (30, 55)
    assert coordinates[-1] == (40, 60)

#на count < 2 ошибка
def test_build_orthodromy_count_less_than_two():
    with pytest.raises(ValueError, match="count must be at least 2"):
        build_orthodromy(30, 55, 40, 60, 1)

#превращается ли список координат в LINESTRING
def test_coordinates_to_wkt():
    coordinates = [(30, 55), (40, 60)]

    result = coordinates_to_wkt(coordinates)

    assert result == "LINESTRING(30 55, 40 60)"