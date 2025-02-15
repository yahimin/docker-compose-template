import requests
from typing import Optional
from main.core.constant import HTTP,HOST,PORT
from main.core._exception import NotFoundException,InternalServerErrorException
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
                raise InternalServerErrorException({'msg' : 'checked origin url'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
                             
        except Exception as e:
            raise NotFoundException({'msg': 'requested client url was not found'}, status=status.HTTP_404_NOT_FOUND)
    @staticmethod
    def verfiy_url_jwt(local_url):
        try:
            host = local_url['HOST'].split(':')
            
            local = host[0]
            port = host[1]
             
            if local != HOST or port != PORT:
                raise InternalServerErrorException({'msg' : 'checked origin url'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)            
            
        except Exception as e:
            raise NotFoundException({'msg' : 'requested jwt url was not found'},status=status.HTTP_404_NOT_FOUND)
           
    @staticmethod
    def decoded_token(token):
        
        pass
