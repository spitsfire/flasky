def test_get_all_breakfasts_with_empty_db_returns_empty_list(client):
    response = client.get("/breakfast")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []
    
def test_get_one_breakfast_with_empty_db_returns_404(client):
    response = client.get("/breakfast/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert "msg" in response_body

def test_get_one_breakfast_with_populated_db_returns_breakfast_json(client, two_breakfasts):
    response = client.get("/breakfast/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name":"Congee",
        "rating":8,
        "prep_time":10
    }

def test_post_one_breakfast_in_empty_creates_breakfast_id_1_in_db(client):
    response = client.post("/breakfast", json={
        "name": "Ada's breakfast special",
        "rating":100,
        "prep_time":0
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "msg" in response_body
    assert response_body["msg"] == "Successfully created Breakfast with id=1"


def test_post_one_breakfast_creates_breakfast_with_new_id_in_db(client, two_breakfasts):
    response = client.post("/breakfast", json={
        "name": "Ada's breakfast special",
        "rating": 100,
        "prep_time":0
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "msg" in response_body
    assert response_body["msg"] == "Successfully created Breakfast with id=3"