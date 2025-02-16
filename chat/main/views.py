from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from main.url_renders import UserRenders
from main.serializers import UserChangePasswordSerializer,UserRegistrationSerializer,UserLoginSerializer,UserDeleteSerializer
from django.shortcuts import render
from main.models import User
from rest_framework.permissions import IsAuthenticated
import random

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from main.core._exception import InternalServerErrorException,BadRequestException,NotFoundException
from main.core._client import HTTPClient



def homepage(request):
    return render(request,'home.html')

def loginpage(request):
    return render(request,'view.html')

def changepage(request):
    return render(request,'chage.html')


    
def get_tokens_users(user):
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
        
        token = RefreshToken.for_user(user)
    
        return {
            'refresh': str(token),
            'access': str(token.access_token),
        }
    except Exception as e:
        raise ImportError('Plase install Simple jwt')
 

        
class HTTPComponent:
    
    @staticmethod
    def init_response(local_url):     
            
        if local_url is not None and 'Authorization' not in local_url:
            HTTPClient.verfiy_url(local_url)        

        elif local_url is not None and 'Authorization' in local_url:
            HTTPClient.verfiy_url_jwt(local_url)

        
            
class UserRegisterView(APIView):
    # 요청 들어오는 필드 값이 빈값인지 유효성 검사
    renderer_classes = [UserRenders]
    
    def post(self,request,format=None):
        
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            users = User.objects.all()            
            client_email = request.data['email']
        
            for user in users:
                if client_email == user.email:
                        raise BadRequestException({'msg': 'Duplicate  email'},status=status.HTTP_400_BAD_REQUEST)
                            
            r"""
                1. check header origin 
            """         
            
            origin = request.headers['Origin']            
            HTTPComponent.init_response(origin)
            
            user = serializer.save()
            
            
            return Response({
                'email' : client_email
            },status=status.HTTP_201_CREATED)

            # return Response({'msg' : 'Register Sucess!'}, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            raise InternalServerErrorException('Server Error!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
class UserListView(APIView):
    
    renderer_classes = [UserRenders]
    
    def get(self,fromat=None):
        try:
            users = User.objects.all()

            users_ids = users.values_list('id','email','name')
            user_data=[]

            for user_id,email,name in users_ids:                
                user_data.append({'id': user_id, 'email' : email , 'name' : name})                        
            
            return Response(user_data, status=status.HTTP_200_OK)

        except Exception as e:
            raise InternalServerErrorException('Server Error!',status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
class UserLoginView(APIView):
    renderer_classes = [UserRenders]
    
    def post(self,request,format=None):
        
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.data.get('email')
        password = serializer.data.get('password')

        user = User.objects.get(email=email)

        try:
            if user.check_password(password):
                token = get_tokens_users(user)
                
                
                access__token = token['access']
                refresh_token = token['refresh']
                
                
                response = JsonResponse({
                    'message' : 'Login Sucess!!',
                })
                
                response.set_cookie('access_token' , access__token,
                httponly=True,
                samesite='Lax'                    
                )
                response.set_cookie('refresh_token', refresh_token,
                httponly=True,
                samesite='Lax'
                )
                r"""
                    1. check header origin 
                """      
                 
                origin = request.headers['Origin']            
                
                HTTPComponent.init_response(origin)
                
                
                
                return response

                # return Response({'token' : token, 'msg' : 'Login Sucess'},status=status.HTTP_200_OK)
            else:
                raise NotFoundException({'msg': 'Email password is incorrect'}, status=status.HTTP_404_NOT_FOUND)
            
        except Exception as e:
            raise InternalServerErrorException('Server Error!' , status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserDeleteView(APIView):
    renderer_classes = [UserRenders]
    
    def post(self,request,format=None):
        
        serializer = UserDeleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            users = User.objects.all()            
            #  삭제할 id 추출 (모델에 존재하는 유니크한 id중 랜덤 추출) 
            id_pair = [(object.id) for object in users]
            
            delete_id = random.choice(id_pair)

            delet_email = User.objects.get(id=delete_id).email            
            
            instance = User.objects.get(id=delete_id)
            instance.delete()
                
            r"""
                1. check header origin 
            """      
                
            origin = request.headers['Origin']            
            HTTPComponent.init_response(origin)
        
            return Response({'msg' : f'Delete {delet_email} Sucess!'} , status=status.HTTP_200_OK)
            
        except Exception as e:
            raise InternalServerErrorException('Servier Error!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UserChangePasswordView(APIView):
    renderer_classes = [UserRenders]
    permission_classes = [IsAuthenticated]
    
    def post(self,request,format=None):
    
        serializer = UserChangePasswordSerializer(data=request.data,context = {'user' : request.user})
        serializer.is_valid(raise_exception=True)


        r"""
            1. check header origin 
            2. check decode user jwt token 
        """        
        HTTPComponent.init_response(request.headers)
                
        return Response({'msg' : 'Password Changed Success!'}, status=status.HTTP_200_OK)
        
        
class UserAccessTokenFromRefreshTokenView(APIView):
        
    def get(self, request):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
                        
            if not refresh_token:
                raise InternalServerErrorException({'msg': 'No refresh token error'})
            
            new_token = RefreshToken(refresh_token)
            
            new_acess_token = str(new_token)
            
            return Response({'msg': f'Refresh token Success {new_acess_token}'})
        
        except Exception as e:
            raise InternalServerErrorException({'msg' : 'Server Error!'})
        

    
