from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self,email,name,tc,password=None,password_second=None):
        
        if not email:
            raise ValueError('User mush have email address')

        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            tc = tc
        )
        
        # 해시된 비밀번호 생성
        user.set_password(password)
        # 디비에 저장 (setting.py DATABASE 'default')
        user.save(using = self._db)
        return user
                


class User(AbstractBaseUser):
    email = models.EmailField(
        name ='Email',
        max_length=255,
        unique=True
    )
    
    name = models.CharField(max_length=200)
    tc = models.BooleanField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
        
    def __str__(self):
        return self.email
    