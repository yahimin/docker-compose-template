from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

####

from main.url_renders import UserRenders
from main.serializers import UserRegistrationSerializer
from django.shortcuts import render

def homepage(request):
    return render(request,'home.html')


def get_tokens_users(user):
    
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
class UserRegisterView(APIView):
    renderer_classes = [UserRenders]
    
    
    def post(self,request,format=None):
        
        print('1@@@@@@@@@@',request.data)
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        user = serializer.save()
            
        try:
            
            print(user)
            token = get_tokens_users(user)
            return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)

        except:
            raise ValueError('Server Error!')
        
    
        
        

        




    
