from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def login(email='admin@meradion.app',password='Admin123!'):
 return client.post('/api/auth/login',json={'email':email,'password':password}).json()['access_token']
def test_health_and_demo_radio():
 assert client.get('/api/health').status_code==200
 assert client.get('/api/radio/now-playing').json()['is_live'] is True
def test_auth_and_authorization():
 assert client.post('/api/auth/login',json={'email':'admin@meradion.app','password':'wrongpass'}).status_code==401
 assert client.post('/api/shows',json={'title':'Test show'}).status_code==401
 h={'Authorization':'Bearer '+login()};assert client.post('/api/shows',headers=h,json={'title':'Test show'}).status_code==201
def test_validation_and_rj_guard():
 assert client.post('/api/auth/register',json={'name':'A','email':'broken','password':'x'}).status_code==422
 h={'Authorization':'Bearer '+login('sai@meradion.app','Radio123!')};assert client.post('/api/shows/1/start',headers=h).status_code==200
