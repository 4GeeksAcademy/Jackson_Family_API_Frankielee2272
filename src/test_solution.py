import pytest, os, tempfile, mock, json
from flask import Flask
@pytest.fixture
def client():
    with mock.patch('flask.Flask', lambda x: Flask(x)):
        from app import app
        db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
        os.close(db_fd)
        os.unlink(app.config['DATABASE'])
@pytest.fixture(autouse=True)
def setup_and_teardown(client):
    # Clear all members before each test if there's an endpoint or method to do so
    # For example, assuming '/clear_all_members' is a valid endpoint:
    client.post('/clear_all_members')  # Ensure this request actually clears members
    # Adding initial set members if needed for every test or handled individually in each test
    yield
    # Optional: clear again if needed after tests
    client.post('/clear_all_members')
@pytest.mark.it("The Family structure has to be initialized with the 3 members specified in the instructions")
def test_first_three(client):
    response = client.get('/members')
    members = json.loads(response.data)
    assert len(members) == 3
@pytest.mark.it("Implement method POST /member to add a new member")
def test_add_implementation(client):
    response = client.post('/member', json={
        "first_name": "Tommy",
        "id": 3443,
        "age": 23,
        "lucky_numbers": [34, 65, 23, 4, 6]
    })
    assert response.status_code == 201
@pytest.mark.it("Method POST /member should return something, NOT EMPTY")
def test_add_empty_reponse_body(client):
    response = client.post('/member', json={
        "first_name": "Sandra",
        "age": 12,
        "id": 4446,
        "lucky_numbers": [12, 34, 33, 45, 32, 12]
    })
    assert response.data
    assert response.get_json() != {}, "Response should not be empty"
@pytest.mark.it("Implement method GET /members")
def test_get_members_exist(client):
    response = client.get('/members')
    assert response.status_code == 200
@pytest.mark.it("Method GET /members should return a list")
def test_get_members_returns_list(client):
    response = client.get('/members')
    data = json.loads(response.data)
    assert isinstance(data, list)
@pytest.mark.it("Method GET /member/<int:id> should exist")
def test_get_single_member_implemented(client):
    response = client.get('/member/3443')
    assert response.status_code == 200
@pytest.mark.it("Method DELETE /member/3443 should return dictionary confirming deletion")
def test_delete_response(client):
    client.post('/member', json={"first_name": "Tommy", "id": 3443, "age": 23, "lucky_numbers": [34, 65, 23, 4, 6]})
    response = client.delete('/member/3443')
    assert 'message' in response.get_json() and response.get_json()['message'] == "Member deleted" #test.solution.py