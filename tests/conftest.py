import pytest


@pytest.fixture
def valid_payload():
    return {
        "seller_id": 1,
        "is_verified_seller": True,
        "item_id": 123,
        "name": "Test Item",
        "description": "Test Description",
        "category": 1,
        "images_qty": 0
    }