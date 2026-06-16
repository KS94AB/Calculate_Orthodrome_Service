import pytest

from app.services.wkt import read_point_wkt

#читается нормально
def test_read_point_wkt_success():
    lon, lat = read_point_wkt("POINT(30 55)")

    assert lon == 30
    assert lat == 55

#вводим неправильные данные
def test_read_point_wkt_invalid_wkt():
    with pytest.raises(ValueError, match="Invalid WKT"):
        read_point_wkt("wrong")

#вводим линию
def test_read_point_wkt_must_be_point():
    with pytest.raises(ValueError, match="WKT must be POINT"):
        read_point_wkt("LINESTRING(30 55, 40 60)")


def test_read_point_wkt_empty_point():
    with pytest.raises(ValueError, match="POINT must not be empty"):
        read_point_wkt("POINT EMPTY")