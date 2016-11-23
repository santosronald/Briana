__author__ = 'klaatu'
from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^vaccines/$', ListVaccinesAPIView.as_view()),
    url(r'^appliedvaccines-child/(?P<child_pk>\d+)/$', ListAppliedVaccinesAPIView.as_view()),
    url(r'^child/(?P<child_pk>\d+)/applied-vaccine/(?P<pk>\d+)/$', RetrieveAppliedVaccineAPIView.as_view()),
    url(r'^child/(?P<child_pk>\d+)/update-applied-vaccine/(?P<pk>\d+)/$', UpdateAppliedVaccineAPIView.as_view()),
    url(r'^centers-related-to-vaccine/(?P<pk>\d+)/$', ListCentersRelatedToVaccineAPIView.as_view()),
    url(r'^diseases-related-to-vaccine/(?P<pk>\d+)/$', ListDiseasesRelatedToVaccineAPIView.as_view()),

]
