from drf_extra_fields.geo_fields import PointField

__author__ = 'klaatu'
from rest_framework import serializers
from .models import Center


class ListCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ('id', 'center_type', 'name', 'address')


class RetrieveCenterSerializer(serializers.ModelSerializer):
    location=PointField()
    class Meta:
        model = Center
        fields = ('id', 'center_type', 'name', 'description', 'address',
                  'location', 'monday_to_friday', 'saturday_sunday_holiday')
