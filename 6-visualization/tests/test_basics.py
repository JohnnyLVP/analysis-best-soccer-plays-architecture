def test_send_ok(client):
    prefix = ''
    response = client.get(prefix + '/')
    assert response.status_code == 200
    assert response.data.decode("utf-8") == 'OK'

