from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from main.url_renders import UserRenders
from main.serializers import UserRegistrationSerializer,UserLoginSerializer,UserDeleteSerializer
from django.shortcuts import render
from main.models import User
from django.contrib.auth import authenticate
import requests


from typing import Optional


import random

from main.core._exception import MethodNotAllowd,InternalServerErrorException,BadRequestException,NotFoundException
from main.core._client import HTTPClient

def lazy_import():
    try:
        from rest_framework_simplejwt.tokens import RefreshToken
    except Exception as e:
        raise ImportError('Plase install Simple jwt')

def homepage(request):
    return render(request,'home.html')

def loginpage(request):
    return render(request,'view.html')

def get_tokens_users(user):
    
    lazy_import()
    from rest_framework_simplejwt.tokens import RefreshToken
    refresh = RefreshToken.for_user(user)
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class HTTPComponent:
    
    @staticmethod
    def init_response(local_url):        
        print('########',local_url)
        
        if local_url is not None:
            HTTPClient.verfiy_url(local_url)
            
            


# TODO [x] : header check class
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
             
             # http header checking (csrf , domain)     
            
            
            origin = request.headers['Origin']            
            HTTPComponent.init_response(origin)
            
            user = serializer.save()
        
            return Response({'msg' : 'Register Sucess!'}, status=status.HTTP_201_CREATED)
            
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
    
    def post(self,request,format=None):
        
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.data.get('email')
        password = serializer.data.get('password')

        user = User.objects.get(email=email)

        try:
            if user.check_password(password):
                token = get_tokens_users(user)
                
                origin = request.headers['Origin']            
                HTTPComponent.init_response(origin)
        
                return Response({'token' : token, 'msg' : 'Login Sucess'},status=status.HTTP_200_OK)
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
            print(users)
            
            
            #  삭제할 id 추출 (모델에 존재하는 유니크한 id중 랜덤 추출) 
            id_pair = [(object.id) for object in users]
            
            delete_id = random.choice(id_pair)

            delet_email = User.objects.get(id=delete_id).email            
            
            instance = User.objects.get(id=delete_id)
            instance.delete()
                
            origin = request.headers['Origin']            
            HTTPComponent.init_response(origin)
        
            return Response({'msg' : f'Delete {delet_email} Sucess!'} , status=status.HTTP_200_OK)
            
        except Exception as e:
            raise InternalServerErrorException('Servier Error!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
        
        
# [] : TODO curl -l 로 비밀번호 패스워드 변경 테스트해보기
class ChangePassword(APIView):
    pass
        




    
