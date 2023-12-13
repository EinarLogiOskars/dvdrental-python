import pytest
import json
from flask_jwt_extended import create_access_token

def test_add_without_token(app, client):
    with app.app_context():
        response = client.post("/films/add", data={
            "title": "Test title",
            "description": "Test description",
            "release_year": "2023",
            "language_id": "1",
            "rental_duration": "1",
            "rental_rate":"1",
            "length":"1",
            "replacement_cost":"1",
            "rating":"PG-13",
            "category":"1",
            "actor":"1",
        })
        assert response.status_code == 401

@pytest.fixture()
def add_with_token(app, client):
    with app.app_context():
        access_token = create_access_token('test_username')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        response = client.post("/films/add", data={
            "title": "Test title",
            "description": "Test description",
            "release_year": "2023",
            "language_id": "1",
            "rental_duration": "1",
            "rental_rate":"1",
            "length":"1",
            "replacement_cost":"1",
            "rating":"PG-13",
            "category":"1",
            "actor":"1",
        }, headers=headers)

        data = dict(status_code = response.status_code, film_id = response.data)

        return data
    
def test_film_added(add_with_token):
    assert add_with_token.get('status_code') == 201

def test_get_film(add_with_token, app, client):
    with app.app_context():
        access_token = create_access_token('test_username')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        route = "/films/film/{}".format(add_with_token.get('film_id').decode('utf-8'))
        response = client.get(route, headers=headers)
        data = json.loads(response.text)

        assert response.status_code == 200
        assert data['title'] == "Test title"

def test_get_film_list_entry(add_with_token, app, client):
    with app.app_context():
        access_token = create_access_token('test_username')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        route = "/films/film_list/{}".format(add_with_token.get('film_id').decode('utf-8'))
        response = client.get(route, headers=headers)
        data = json.loads(response.text)

        assert response.status_code == 200
        assert data['title'] == "Test title"

def test_remove_film(add_with_token, app, client):
    with app.app_context():
        access_token = create_access_token('test_username')
        headers = {
            'Authorization' : 'Bearer {}'.format(access_token)
        }
        response = client.post("films/remove", data = {
            'film_id': add_with_token.get('film_id').decode('utf-8')
        }, headers=headers)

        assert response.status_code == 200
        assert response.data == "Affected rows: 1"

#TODO: finish implementing this test function
#def test_get_film_list(app, client):
#    with app.app_context():
#        access_token = create_access_token('test_username')
#        headers = {
#            'Authorization': 'Bearer {}'.format(access_token)
#        }
#        response = client.get('/films/film_list', headers = headers)
#        data = json.loads(response.text)
#
#        assert response.status_code == 200