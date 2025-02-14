import requests


from typing import Optional
from main.core.constant import HTTP,HOST,PORT
from main.core._exception import NotFoundException
from rest_framework import status

class HTTPClient:
    
    @staticmethod
    def verfiy_url(local_url):
        try:
            from urllib.parse import urlparse            
            pared_url = urlparse(local_url)
            domain_name = pared_url.netloc.split(':')
            
            local = domain_name[0]
            port = domain_name[1]
            scheme = pared_url.scheme
            
            if local != HOST or port != PORT or scheme != HTTP:
                return False            
                             
        except Exception as e:
            raise NotFoundException({'msg': 'request client not found'}, status=status.HTTP_404_NOT_FOUND)
            

