import pytest

from app.services.crs import (
    validate_crs,
    transform_point_to_wgs84,
    transform_point_from_wgs84
)
#проверяем срабатывание фунции валидации - корректное значение
def test_validate_crs_correct_value():
    validate_crs(4326)

#проверяем срабатывание фунции валидации - некорректное значение
def test_validate_crs_wrong_value():
    with pytest.raises(ValueError):
        validate_crs(9999)
#при входной проекции EPSG:4326, координаты должны возвращаться без изменений 
def test_4326_to_wgs84():
    lon, lat = transform_point_to_wgs84(37.6173, 55.7558, 4326)
    assert lon == 37.6173
    assert lat == 55.7558

# успешный перевод из СК-42 в wgs84
def test_sk42_to_wgs84():
    lon, lat = transform_point_to_wgs84(37.619174, 55.755757, 4284)
    assert round(lon, 2) == 37.62
    assert round(lat, 2) == 55.76

#успешный перевод в проекцию mercator
def test_wgs84_to_mercator():
    x, y = transform_point_from_wgs84(37.6173, 55.7558, 3857)
    assert round(x, 2) == 4187538.68
    assert round(y, 2) == 7509955.14

#успешный перевод из mercator в wgs84
def test_mercator_to_wgs84():
    lon, lat = transform_point_to_wgs84(4187538.68, 7509955.14, 3857)
    assert round(lon, 4) == 37.6173
    assert round(lat, 4) == 55.7558