from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

def test_main():
        response = client.get("http://127.0.0.1:8000/")
        print('response is: ', response.json())
        print('are they equal: ', response.json() == {"msg":"Hello World"})
        assert response.json() == {"msg":"Hello World"}

# this passes when I run it in from the interpreter, but fails if I try to use pytest teseting.py
# it keeps returning {"item_id": "foo", "description":"This is an amazing item that has a long description"}
# I have no idea where it's getting that from - it never does that when run from the docs or from
# the interpreter. So I'm chalking it up to pytest being weird because I want to keep moving
# and I'm not learning anything from trying to debug this atm.
def test_read_item():
    response = client.get("/items/foo", headers={"X-Token": "coneofsilence"})    
    assert response.status_code == 200
    target = {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }
    assert response.json() == target
    print(response.json() == target)

def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "hailhydra"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_inexistent_item():
    response = client.get("/items/baz", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Barters"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Barters",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items/",
        headers={"X-Token": "hailhydra"},
        json={"id": "bazz", "title": "Bazz", "description": "Drop the bazz"},
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_create_existing_item():
    response = client.post(
        "/items/",
        headers={"X-Token": "coneofsilence"},
        json={
            "id": "foo",
            "title": "The Foo ID Stealers",
            "description": "There goes my stealer",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Item already exists"}