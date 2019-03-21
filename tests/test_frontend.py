from transcribe import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_frontend(client, app):
    assert client.get('/transcribe/').status_code == 200

    response = client.get('/transcribe/')
    assert b"Transkripce" in response.data
    assert "vložte větu pro transkripci do IPA" in response.get_data(as_text=True)

def test_frontend_post(client, app):
    response = client.post('/transcribe/', data={'source_text': 'vložte větu pro transkripci do IPA', 'target_text': ''})
    assert "vloʒtɛ vjɛtu pro transkrɪpt͡sɪ do ʔɪpa" in response.get_data(as_text=True)
