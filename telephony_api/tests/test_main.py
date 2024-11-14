from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_get_phone_bill_without_period():
    response = client.get('/phone-bill/48999650061')

    assert response.status_code == 200

    data = response.json()
    assert 'phone_number' in data
    assert data['phone_number'] == '48999650061'
    assert 'period' in data
    assert 'total_cost' in data
    assert data['total_cost'] == '0.00'
    assert 'records' in data
    assert isinstance(data['records'], list)


def test_get_phone_bill_with_period():
    response = client.get('/phone-bill/48999650061?period=2024-10-01')

    assert response.status_code == 200

    data = response.json()
    assert 'period' in data
    assert data['period'] == '2024-10-01'

    assert 'total_cost' in data
    assert data['total_cost'] != '0.00'
    assert 'records' in data
    assert len(data['records']) > 0


def test_get_phone_bill_for_nonexistent_number():
    response = client.get('/phone-bill/12345678900')

    assert response.status_code == 404
    data = response.json()
    assert 'detail' in data
    assert data['detail'] == 'Phone number not found'


def test_get_phone_bill_with_invalid_period():
    response = client.get('/phone-bill/48999650061?period=invalid-period')

    assert response.status_code == 400
    data = response.json()
    assert 'detail' in data
    assert data['detail'] == 'Invalid period format'
