from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name="home"),
    path('login/', views.signInPage, name='login'),
    path('signup/', views.signUpPage, name='signup'),
    path('chat/<int:pk>/', views.chatPage, name='chat'),
]
