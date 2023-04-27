import pytest
import requests

# User CRUD Opertations 

def test_create_user():
    url = "http://0.0.0.0:8080/api/client"

    payload = {
        "email": "test@example.com",
        "password": "password",
        "role": "Student"
    }

    response = requests.post(url, data=payload)

    # Assert that the request-response cycle completed successfully.
    assert response.status_code == 201

    # Assert that the response body is what we expect.
    assert response.json()["email"] == "test@example.com"
    assert response.json()["password"] == "password"
    assert response.json()['role_details']["role_name"] == "Student"

def test_get_user_all():
    url = "http://0.0.0.0:8080/api/client"

    response = requests.get(url)
    print(response.text)

    # Assert that the request-response cycle completed successfully.
    assert response.status_code == 200

def test_get_user_unique():
    url = "http://0.0.0.0:8080/api/client/1"

    response = requests.get(url)
    print(response.text)


    # Assert that the request-response cycle completed successfully.
    assert response.status_code == 200

def test_put_user():
    url = "http://0.0.0.0:8080/api/client/1"

    payload = {
        "id": "1",
        "email": "updated@example.com",
        "password": "newpassword",
        "role": "Student"
    }


    response = requests.put(url, data=payload)

    # Assert that the request-response cycle completed successfully.
    assert response.status_code == 200

    # Assert that the response body is what we expect.
    assert response.json()["email"] == "updated@example.com"

def test_delete_user():
    url = "http://0.0.0.0:8080/api/client/1"

    response = requests.delete(url)
    print(response.text)


    # Assert that the request-response cycle completed successfully.
    assert response.status_code == 200

# Testing Query and FAQ 

def create_query():
    url = "http://0.0.0.0:8080/api/query"

    payload = {
        'issue': "Test Issue",
        'solution': "No Solution",
        'created_by': "test@exampple.com",
        'answered_by': "None",
        'upvotes': 0,
    }


    response = requests.post(url, data=payload)

    # Assert that the request-response cycle completed successfully.
    assert response.status_code == 201

    # # Assert that the response body is what we expect.
    assert response.json()["issue"] == "Test Issue"
    assert response.json()["solution"] == "No Solution"
    assert response.json()["created_by"] == "test@exampple.com"
    assert response.json()["answered_by"] == "None"

def create_faq():
    url = "http://0.0.0.0:8080/api/faq"

    payload = {
        'issue': "Test Issue",
        'solution': "Solution",
        'upvotes': 0,
    }


    response = requests.post(url, data=payload)
    print(response.text)

    # Assert that the request-response cycle completed successfully.
    assert response.status_code == 201

    # # Assert that the response body is what we expect.
    assert response.json()["issue"] == "Test Issue"
    assert response.json()["solution"] == "No Solution"


# if __name__ == "__main__":
#     create_faq()
