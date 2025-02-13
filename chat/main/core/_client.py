import requests
from typing import Optional



class HTTPClient:
    
    def __init__(self, csrf: Optional[str] = None , domain: str = '' , user_agent: str =''):
        # csrf token        
        self._init_csrf_token(csrf)
        self._init_local(domain)
        self._init_agent(user_agent)
    
    
    def _init_csrf_token(self,csrf):        
        print('5###########',csrf)
        pass

    def _init_local(self,local_url):
        pass
        
    def _init_agent(self,user_agent):
        pass



class AsyncHTTPClinet(HTTPClient):
    
    @staticmethod
    async def check_response_header(response: requests.Response):
        r"""
            check_response_header is a helper 
        """
        pass    
