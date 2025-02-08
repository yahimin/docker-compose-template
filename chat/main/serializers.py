from rest_framework import serializers

from main.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'name' , 'password','password_second','tc']
        
        # password 필드 쓰기만 가능하게 (사용자가 데이터를 전송할때는 필드에 값을 쓸수있지만 , 응답으로 데이터를 보낼때는 필드가 포함되지 않게)
        extra_kwargs={
            'password' : {'write_only': True}
        }
        # 직렬화 데이터를 유효성 검사
        
        # 1. 1차 2차 비밀번호 동일하지 않으면 에러
        # 2. 패스워드 8자 이상이면 에러
        # 3. 숫자로만 이루어져있으면 에러
        def validate(self,attrs):
            password = attrs.get('password')
            password_second = attrs.get('password_second')
            
            if password != password_second:
                return serializers.ValidationError('Password and Confirm do not match')
        
            if len(password) > 8:
                raise ValueError('User Password len is incorrect')

            if password.isdigit():
                raise ValueError('User Password is entirely numberic')

            return attrs


        # 직렬화 데이터 유효성검사를 마친 후 데이터
        # key-value 쌍을 인자로 풀어서 전달 **validate_data
        # email = 'hwan' , password = 123123
        def create(self,validate_data):
            return User.objects.create_user(**validate_data)
        
        