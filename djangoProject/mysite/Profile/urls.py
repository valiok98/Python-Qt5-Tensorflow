from django.shortcuts import render
from django.conf.urls import url
from . import views,models
# Create your views here.

app_name = 'Profile'

urlpatterns = [


    url(r'^$',views.profile, name='profile'),
    url(r'^(?P<user_id>[0-9]+)/$', views.items, name='users'),
    url(r'^sign_in/$', views.signin, name='signin'),
    url(r'^sign_up/$', views.signup, name='signup'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^edit/(?P<id>[0-9]+)/$', views.edit_form, name='edit_person'),
    url(r'^delete/(?P<id>[0-9]+)/$', views.delete, name='delete')

]
