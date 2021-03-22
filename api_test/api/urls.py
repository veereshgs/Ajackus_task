from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('user_register/', FormSignupApi.as_view(), name="user_register"),
    path('login/api/', UserLoginView.as_view(), name='login'),
    path('content_api/', ContentAPI.as_view(), name='content_api'),
    path('content_data/', ContentGetAPI.as_view(), name="content_data"),

]
