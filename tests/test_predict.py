import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#1.Положительные тесты (200 OK)


def test_predict_verified_seller_no_violation(valid_payload):
    payload = {**valid_payload, "is_verified_seller": True, "images_qty": 0}
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert response.json() == {"is_violation": False}


def test_predict_unverified_seller_with_images_no_violation(valid_payload):
    payload = {**valid_payload, "is_verified_seller": False, "images_qty": 3}
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert response.json() == {"is_violation": False}


#2.Отрицательный тест (200 OK, но есть нарушение)

def test_predict_unverified_seller_no_images_violation(valid_payload):

    payload = {**valid_payload, "is_verified_seller": False, "images_qty": 0}
    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    assert response.json() == {"is_violation": True}


#3.Тесты валидации обязательных полей

@pytest.mark.parametrize("missing_field", [
    "seller_id",
    "is_verified_seller",
    "item_id",
    "name",
    "description",
    "category",
    "images_qty"
])
def test_predict_missing_required_field(valid_payload, missing_field):

    payload = valid_payload.copy()
    del payload[missing_field]

    response = client.post("/predict", json=payload)
    assert response.status_code == 400


#4.Тесты валидации типов и значений

@pytest.mark.parametrize("invalid_data", [
    {"seller_id": "not_an_int"},
    {"is_verified_seller": "not_a_bool"},
    {"name": ""},
    {"images_qty": -1}
])
def test_predict_invalid_types_and_values(valid_payload, invalid_data):

    payload = {**valid_payload, **invalid_data}
    response = client.post("/predict", json=payload)
    assert response.status_code == 400


#5.Тест обработки ошибки бизнес-логики

def test_predict_business_logic_error(valid_payload):

    payload = {**valid_payload, "item_id": 0}
    response = client.post("/predict", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Item ID cannot be zero in business logic"