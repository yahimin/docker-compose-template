import pytest
import requests
import jwt
from rest_framework.test import APIClient


####################################### fixure ########################################
@pytest.fixture
def base_url():
    return 'http://localhost:8000'

@pytest.fixture
def base_header():
    headers = {
        'Content-Type' : 'application/json',
        'Origin' : 'http://localhost:8000'
    }    
    return headers



@pytest.fixture
def jwt_token():
    token = get_token()    
    print(token)
    return token



####################################### utils ########################################
def barer_auth_header(token):
    
    headers = {
        'Content-Type' : 'application/json',
        'Origin' : 'http://localhost:8000',
        'Authorization' : f'Bearer {token}'
    }
        
    return headers    


def get_token():
    
    base_url = 'http://localhost:8000'
    api = '/login/api/signin'
    
    url = f'{base_url}/{api}'
    
    headers = {
        'Content-Type' : 'application/json',
        'Origin' : 'http://localhost:8000'
    }   
    
    payloads = {
        'email' : 'x2221@nate.com',
        'password' : '12a',
    }
    
    
    response = requests.post(url,json = payloads,headers=headers)
    
    
    return response.cookies.get_dict()['access_token']

##################################### test #########################################
@pytest.mark.parametrize('url',[
    'api/users'  
])


def test_api(base_url,url):
   
    response = requests.get(f'{base_url}/{url}')
    r_j = response.json()[0]
    
    payload = {
        'id' : 43,
        'email' : 'ghks144444444444444444423@nate.com',
        'name' : '123'
    }

    if response.status_code == 200:
        if payload == r_j:    
            assert payload['id'] == r_j['id']
            assert payload['email'] == r_j['email']
            assert payload['name'] == r_j['name']

    else:
        pytest.fail()
      
@pytest.mark.parametrize('url',[
    'api/register'
])  

def test_register(base_url,url,base_header):
    
    headers = base_header
    
    dummy_user = {
        'email' : 'x2221@nate.com',
        'name' : 'seung',
        'password' : '123a',
        'password_second' : '123a'
    }
                
    response = requests.post(f'{base_url}/{url}', json=dummy_user, headers=headers)    
    r = response.json()    
    
    if response.status_code == 201:
        print('Sucess')
        # assert r.headers.get('email') == 'hi4253@nate.com'
        assert r['email'] == 'x2221@nate.com'
    else:
        pytest.fail()
        
        

@pytest.mark.parametrize('url',[
    'api/delete'
])  

def test_deleted_user(base_url,url,base_header):
 
    headers = base_header
        
    dummy_id = {}

    response = requests.post(f'{base_url}/{url}',json=dummy_id,headers=headers)    
    
    if response.status_code == 200:
        print('delete sucess')
        assert response.status_code == 200
    else:
        pytest.fail() 



@pytest.mark.parametrize('url',[
    '/login/api/signin'
])  

def test_login(base_url,url,base_header):
    
    headers = base_header
    
    dummy_user ={
        'email' : 'x2221@nate.com',
        'password' : '123a',
    }
    
    response = requests.post(f'{base_url}/{url}',json = dummy_user,headers=headers)
    
    if response.status_code == 200:        
        jwt_acess_token = response.cookies.get_dict()['access_token']
        jwt_refresh_token = response.cookies.get_dict()['refresh_token']

        decoded1 = jwt.decode(jwt_acess_token, options = {'verify_signature' : False})
        decoded2 = jwt.decode(jwt_refresh_token,options = {'verify_signature': False})

        assert decoded1['token_type'] == 'access'
        assert decoded2['token_type'] == 'refresh'
    else:
        pytest.fail()
        

@pytest.mark.parametrize('url',[
    'change/api/update'
])

def test_update_password(base_url,url,base_header,jwt_token):
    
    headers = base_header
    
    dummy_user ={
        'email' : 'x2221@nate.com',
        'password' : '12a',
        'password_second' : '123a'
    }    
    

    barer_header = barer_auth_header(jwt_token)
    response = requests.post(f'{base_url}/{url}',json=dummy_user,headers=barer_header)
        
    assert response.status_code == 200

