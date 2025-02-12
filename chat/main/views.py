from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.url_renders import UserRenders
from main.serializers import UserRegistrationSerializer
from django.shortcuts import render
from main.models import User

from main.core._exception import InternalServerErrorException , BadRequestException

def lazy_import():
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
    
    except Exception as e:
        raise ImportError('Plase install Simple jwt')

def homepage(request):
    return render(request,'home.html')

def get_tokens_users(user):
    
    lazy_import()
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
    
    
 # TODO : [x] : 회원가입 중복 이메일 못들어가게 막기   
class UserRegisterView(APIView):
    renderer_classes = [UserRenders]
    

    def post(self,request,format=None):
        
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    

        users = User.objects.all()
        
        client_email = request.data['email']
        
        for user in users:
            if client_email == user.email:
                    raise BadRequestException({'msg': 'Duplicate  email'},status=status.HTTP_400_BAD_REQUEST)

        
        user = serializer.save()
            
        try:
            token = get_tokens_users(user)
            return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)

        except Exception as e:
            raise InternalServerErrorException('Server Error!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class UserListView(APIView):
    renderer_classes = [UserRenders]
    
    def get(self,fromat=None):
        try:
            users = User.objects.all()
            user_data=[]
            
            for user in users:
                to_email = user.email
                to_name = user.name
                
                user_data.append({'email' : to_email , 'name' : to_name})
            
            
            return Response(user_data, status=status.HTTP_200_OK)

        except Exception as e:
            raise InternalServerErrorException('Server Error!',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
class UserLoginView(APIView):
    
    renderer_classes = [UserRenders]
    


        
    
        
        

        




    
