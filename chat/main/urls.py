from django.urls import path ,include
from main.views import UserRegisterView , UserListView

from rest_framework import routers

from . import views

urlpatterns = [ 
    path('',views.homepage, name='homepage'),
    path('api/register/',UserRegisterView.as_view(),name ='register'),
    path('api/users',UserListView.as_view() , name='users'),
]

