from rest_framework import serializers
from main.models import User
from rest_framework import status
from rest_framework.response import Response
from main.core._exception import InternalServerErrorException , BadRequestException

class UserRegistrationSerializer(serializers.ModelSerializer):
    password_second = serializers.CharField(required=False)
    class Meta:
    
        model = User
            
        fields = ['email', 'name' , 'password','password_second']
        
        r""" 
            password 필드 쓰기만 가능하게 (사용자가 데이터를 전송할때는 필드에 값을 쓸수있지만 ,
            응답으로 데이터를 보낼때는 필드가 포함되지 않게) => 비밀번호 숨기기
        """
        
        extra_kwargs={
            'password' : {'write_only': True},
        }
        
    r""""
        직렬화 데이터를 유효성 검사
        
        # 1. 1차 2차 비밀번호 동일하지 않으면 에러
        # 2. 패스워드 8자 이상이면 에러
        # 3. 숫자로만 이루어져있으면 에러
        
    """
  
    def validate(self,attrs):
            api_type_set = {'email', 'name' , 'password' , 'password_second'}
        
            api_type_filter = list(attrs.keys())
            
            if not set(api_type_filter).issubset(api_type_set):
                raise InternalServerErrorException(f'msg : mismacted set filed , expected in {api_type_set}')
        
            password = attrs.get('password')
            password_second = attrs.get('password_second')
            
                    
            if password != password_second:
                raise BadRequestException({'msg' : 'Password and Confirm do not match'},status=status.HTTP_400_BAD_REQUEST)
        
            if len(password) > 8 or len(password_second) > 8:
                raise BadRequestException({'msg': 'User password len is incorrect'}, status=status.HTTP_400_BAD_REQUEST)

            if password.isdigit() or password_second.isdigit():
                raise BadRequestException({'msg': 'User password is entirely numberic'}, status=status.HTTP_400_BAD_REQUEST)

            return attrs

    r"""
        직렬화 데이터 유효성 검사를 마친 후 데이터 key-value 쌍을 인자로 풀어서 전달(**validate_data)
        email = 'hwan' , password = 123421
    """

    def create(self,validate_data):            
        return User.objects.create_user(**validate_data)
        

class UserDataListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        
        fields = ['email','name']
        
        extra_kwargs={
            'password' : {'write_only': True},
        }
        
    
    r"""
        요청들어오는 필드가 존재하는지 확인 
    """
    
    def validate(self,attrs):
        api_type_set = {'email', 'name'}

        api_type_fileter = list(attrs.keys())
            
        if not set(api_type_fileter).issubset(api_type_set):
            raise InternalServerErrorException(f'mismacted set filed , expected in {api_type_set}')
            
class UserLoginSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    
    class Meta: 
        model = User
        fields = ['email','password']
    
        
    def validate(self,attrs):
        api_type_set = {'email', 'password'} 
        api_type_fileter = list(attrs.keys())
            
        if not set(api_type_fileter).issubset(api_type_set):
            raise InternalServerErrorException(f'mismacted set filed , expected in {api_type_set}')       

        return attrs

class UserDeleteSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        
        fields = ['id']
        
        
class UserChangePasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(required=False)
    password_second = serializers.CharField(required=False)
    
    class Meta:
        model = User
        fields = ['password','password_second']
        
        
        extra_kwargs={
            'password' : {'write_only': True},
        }
        
    
    def validate(self,attrs):            
        password = attrs.get('password')
        new_password = attrs.get('password_second')
        
        if password == new_password:
            raise BadRequestException({'msg' : 'match password'},status=status.HTTP_400_BAD_REQUEST)
        
        user = self.context.get('user')
            
        user.set_password(new_password)
        user.save()
            
        return attrs