from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('geting_started', views.index),
    path('create_message', views.create_message),
    path('create_comment', views.create_comment)
]