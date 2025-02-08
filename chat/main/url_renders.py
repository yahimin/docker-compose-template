from rest_framework import renderers
import json

# 클라이언트 requeset 데이터를 json으로 렌더링해서 오류 검사하고 다시 repsonse 
class UserRenders(renderers.JSONRenderer):   
    charset='utf-8'
    
    def render(self,data,accepted_media_type=None, renderer_context=None):
        response =''
        
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors' :data},ensure_ascii=False)
            
        # 한글이 유니코드로 변환되지 않도록
        else:
            response = json.dumps(data, ensure_ascii=False)
        
        return response