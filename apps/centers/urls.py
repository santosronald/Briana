__author__ = 'klaatu'
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^centers/$', ListCenterAPIView.as_view()),
    url(r'^centers/(?P<pk>\d+)/$',RetrieveCenterAPIView.as_view()),
]
