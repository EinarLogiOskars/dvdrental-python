import pytest
from flask_jwt_extended import create_access_token

def test_register(client):
    response = client.post("/auth/register", data={
        "username": "test_username",
        "password": "test_password",
        "email": "test@email.test",
        "first_name": "Test",
        "last_name": "Test",
    })
    assert response.status_code == 201

def test_register_duplicate(client):
    response = client.post("/auth/register", data={
        "username": "test_username",
        "password": "test_password",
        "email": "test@email.test",
        "first_name": "Test",
        "last_name": "Test",
    })
    assert response.status_code == 200 and response.data == b'User test_username is already registered.'

def test_login(client):
    response = client.post("/auth/login", data={
        "username": "test_username",
        "password": "test_password",
    })
    assert response.status_code == 200

def test_login_incorrect_username(client):
    response = client.post("/auth/login", data={
        "username": "wrong_test_username",
        "password": "test_password",
    })
    assert response.status_code == 401

def test_login_incorrect_password(client):
    response = client.post("/auth/login", data={
        "username": "test_username",
        "password": "wrong_test_password",
    })
    assert response.status_code == 401

def test_disable(app, client):
    with app.app_context():
        access_token = create_access_token('test_username')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post('/auth/disable', data={"username": "test_username"}, headers=headers)
        assert response.status_code == 200

def test_remove(app, client):
    with app.app_context():
        access_token = create_access_token('test_username')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post('/auth/remove', headers=headers, data={"username": "test_username"})

        assert response.status_code == 200 and response.data == b"Affected rows: 1"

def test_remove_nonexistent(app, client):
    with app.app_context():
        access_token = create_access_token('test_username')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post('/auth/remove', headers=headers, data={"username": "test_username"})

        assert response.status_code == 200 and response.data == b"Affected rows: 0"

def test_logout(app, client):
    with app.app_context():
        access_token = create_access_token('test_username')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post('/auth/logout', headers=headers, data={"username": "test_username"})

        assert response.status_code == 200