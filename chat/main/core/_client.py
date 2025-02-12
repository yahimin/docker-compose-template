import requests
r"""
    Slow I/O bound
    => 네트워크 요청시 알수없는 네트워크 지연에 대비해서 비동기로 처리 
    => 또한 i/o바운드는 경쟁조건에 대비할 필요가 없기에 
    
    (i/o 바운드는 cpu 성능보다는 네트워크 , 데이터베이스 , 처리속도에 의해 성능이 결정됨)
    
"""

class AsyncHTTPClinet():
    
    @staticmethod
    async def check_response_header(response: requests.Response):
        r"""
            check_response_header is a helper 
        """
    
        pass
