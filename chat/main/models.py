from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self,email,name,password=None,password_second=None):
        
        if not email:
            raise ValueError('User mush have email address')

        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
        )
        
        r""" 해시된 비밀번호 생성 """
        user.set_password(password)
        
        r""" 디비에 저장 setting.py Database 'default' """
        user.save(using = self._db)
        return user
                
r""" 자동으로 password , last_login 필드 모델에 적용되게 AbstractBaseUser 상속 """
class User(AbstractBaseUser):
    email = models.EmailField(
        default='email',
        max_length=255)
    name = models.CharField(max_length=200)

    password_seconde = models.CharField(default='password_second',max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
        
    def __str__(self):
        return self.email
    