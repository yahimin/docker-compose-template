from django.urls import path ,include
from main.views import UserRegisterView

from rest_framework import routers

from . import views

urlpatterns = [ 
    path('',views.homepage, name='homepage'),
    path('api/register/',UserRegisterView.as_view(),name ='register'),
]

