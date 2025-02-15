import pytest
import requests
import json


@pytest.fixture
def base_url():
    return 'http://localhost:8000'

@pytest.mark.parametrize('url',[
    'api/users'  
])

def test_api(base_url,url):    
    assert requests.get(f'{base_url}/{url}').status_code==200
      
        
@pytest.mark.parametrize('url',[
    'api/register'
])  

def test_register(base_url,url):
    
    headers = {
        'Content-Type' : 'application/json',
        'Origin' : 'http://localhost:8000'
    }
    
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
    ('api/delete')
])  

def test_deleted_user(base_url,url):
    
    headers = {
        'Content-Type' : 'application/json',
        'Origin' : 'http://localhost:8000'
    }
        

    dummy_id = {}

    response = requests.post(f'{base_url}/{url}',json=dummy_id,headers=headers)    
    
    if response.status_code == 200:
        print('delete sucess')
        assert response.status_code == 200
    else:
        pytest.fail() 
    
