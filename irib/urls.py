from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.home, name='home'),
    path('process', views.process, name='process'),
    url(r'^validate/(?P<trans>.+)/$', views.validate, name='validate'),
    url(r'^feed/(?P<sent_text>.+)/(?P<actual_state>.+)/(?P<word_position>.+)/$', views.feed, name='feed'),
    # path('feed/<int:actual_state>/<int:word_position>/<str:sent_text>', views.feed, name='feed')
]