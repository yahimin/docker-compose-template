from django.urls import path ,include
from main.views import UserRegisterView , UserListView , UserLoginView , UserDeleteView , UserChangePasswordView , UserAccessTokenFromRefreshTokenView

from rest_framework import routers

from . import views

urlpatterns = [ 
    path('change/',views.changepage , name = 'changepage'),
    path('',views.homepage, name='homepage'),
    path('login/',views.loginpage, name ='loginpage'),
    path('api/register',UserRegisterView.as_view(),name ='register'),
    path('api/users',UserListView.as_view() , name='users'),
    path('login/api/signin',UserLoginView.as_view(),name='login'),
    path('api/delete' , UserDeleteView.as_view(), name = 'delete'),
    path('change/api/update',UserChangePasswordView.as_view() , name='change'),
    path('api/refresh' , UserAccessTokenFromRefreshTokenView.as_view(), name = 'refresh'),
]

