import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    return app.test_client()

#страница открывается
def test_index_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Calculate Orthodrome Service" in response.get_data(as_text=True)

#проверка работы
def test_orthodromy_success_text_response(client):
    response = client.get("/orthodromy", query_string={
        "point1": "POINT(30 55)",
        "point2": "POINT(40 60)",
        "cs": "4326",
        "count": "5"
    })

    text = response.get_data(as_text=True)

    assert response.status_code == 200
    assert text.startswith("LINESTRING(")

#проверка данных для построения на карте
def test_orthodromy_success_json_response(client):
    response = client.get("/orthodromy", query_string={
        "point1": "POINT(30 55)",
        "point2": "POINT(40 60)",
        "cs": "4326",
        "count": "5",
        "format": "json"
    })

    data = response.get_json()

    assert response.status_code == 200
    assert data["wkt"].startswith("LINESTRING(")
    assert data["map_wkt"].startswith("LINESTRING(")
    assert data["cs"] == 4326
    assert data["count"] == 5

#нет одного параметра
def test_orthodromy_missing_point1(client):
    response = client.get("/orthodromy", query_string={
        "point2": "POINT(40 60)",
        "cs": "4326",
        "count": "5"
    })

    assert response.status_code == 400
    assert "point1 parameter is required" in response.get_data(as_text=True)

#нет одного параметра
def test_orthodromy_missing_point2(client):
    response = client.get("/orthodromy", query_string={
        "point1": "POINT(30 55)",
        "cs": "4326",
        "count": "5"
    })

    assert response.status_code == 400
    assert "point2 parameter is required" in response.get_data(as_text=True)

#нет одного параметра
def test_orthodromy_missing_count(client):
    response = client.get("/orthodromy", query_string={
        "point1": "POINT(30 55)",
        "point2": "POINT(40 60)",
        "cs": "4326"
    })

    assert response.status_code == 400
    assert "count parameter is required" in response.get_data(as_text=True)

#неправильный wkr параметр
def test_orthodromy_invalid_wkt(client):
    response = client.get("/orthodromy", query_string={
        "point1": "wrong",
        "point2": "POINT(40 60)",
        "cs": "4326",
        "count": "5"
    })

    assert response.status_code == 400
    assert "Invalid WKT" in response.get_data(as_text=True)

#неправильный тип геометрии wkt
def test_orthodromy_wkt_must_be_point(client):
    response = client.get("/orthodromy", query_string={
        "point1": "LINESTRING(30 55, 40 60)",
        "point2": "POINT(40 60)",
        "cs": "4326",
        "count": "5"
    })

    assert response.status_code == 400
    assert "WKT must be POINT" in response.get_data(as_text=True)

#неправильная система координат
def test_orthodromy_invalid_cs(client):
    response = client.get("/orthodromy", query_string={
        "point1": "POINT(30 55)",
        "point2": "POINT(40 60)",
        "cs": "9999",
        "count": "5"
    })

    assert response.status_code == 400
    assert "CRS must be 4326, 4284 or 3857" in response.get_data(as_text=True)

#cs должно быть int
def test_orthodromy_cs_must_be_integer(client):
    response = client.get("/orthodromy", query_string={
        "point1": "POINT(30 55)",
        "point2": "POINT(40 60)",
        "cs": "abc",
        "count": "5"
    })

    assert response.status_code == 400
    assert "cs must be integer" in response.get_data(as_text=True)

#count должно быть int
def test_orthodromy_count_must_be_integer(client):
    response = client.get("/orthodromy", query_string={
        "point1": "POINT(30 55)",
        "point2": "POINT(40 60)",
        "cs": "4326",
        "count": "abc"
    })

    assert response.status_code == 400
    assert "count must be integer" in response.get_data(as_text=True)

#count >= 2
def test_orthodromy_count_less_than_two(client):
    response = client.get("/orthodromy", query_string={
        "point1": "POINT(30 55)",
        "point2": "POINT(40 60)",
        "cs": "4326",
        "count": "1"
    })

    assert response.status_code == 400
    assert "count must be at least 2" in response.get_data(as_text=True)