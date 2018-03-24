from django.shortcuts import render
from django.conf.urls import url
from . import views,models
# Create your views here.

app_name = 'Profile'

urlpatterns = [


    url(r'^$',views.profile, name='profile'),
    url(r'^(?P<user_id>[0-9]+)/$', views.items, name='users'),

]
