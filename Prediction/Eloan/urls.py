from django.urls import path
from Eloan.views import *
urlpatterns = [
    path('',wellcome,name='music'),
    path('signin',signin,name='signin'),
    path('login',login,name='login'),
    path('logout',logout,name='logout'),
    path('home',home,name='home'),
    path('prediction',prediction,name='prediction'),
    path('team',team,name='team')
]