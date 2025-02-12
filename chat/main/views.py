from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.url_renders import UserRenders
from main.serializers import UserRegistrationSerializer , UserDataListSerializer
from django.shortcuts import render


from main.core._exception import InternalServerErrorException

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
    
    
 # TODO : [] : 회원가입 중복 이메일 못들어가게 막기 (MYSQL에 이메일만 저장해서 관리하고 중복검사)    
class UserRegisterView(APIView):
    renderer_classes = [UserRenders]
    

    def post(self,request,format=None):
        
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
    
        user = serializer.save()
            
        try:
            token = get_tokens_users(user)
            print(token) 

            return Response({'token':token,'msg':'Registration Success'},status=status.HTTP_201_CREATED)

        except Exception as e:
            raise InternalServerErrorException('Server Error!')
    
class UserListView(APIView):
    renderer_classes = [UserRenders]
    
    def get(self,fromat=None):
        try:
            from main.models import User
            
            users = User.objects.all()
            user_data=[]
            
            for user in users:
                to_email = user.email
                to_name = user.name
                
                user_data.append({'email' : to_email , 'name' : to_name})
            
            
            return Response(user_data, status=status.HTTP_200_OK)

        except Exception as e:
            raise InternalServerErrorException('Server Error!')
            
        



        
    
        
        

        




    
