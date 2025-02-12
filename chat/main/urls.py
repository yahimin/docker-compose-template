from django.urls import path ,include
from main.views import UserRegisterView , UserListView , UserLoginView

from rest_framework import routers

from . import views

urlpatterns = [ 
    path('',views.homepage, name='homepage'),
    path('login/',views.loginpage, name ='loginpage'),
    path('api/register',UserRegisterView.as_view(),name ='register'),
    path('api/users',UserListView.as_view() , name='users'),
    path('login/api/signin',UserLoginView.as_view(),name='login'),
]

