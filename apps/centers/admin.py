from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import *
from .forms import GisForm


class CenterAdmin(OSMGeoAdmin):
    list_display = ("center_type", "name", "address",)
    search_fields = ['center_type',]
    form = GisForm

admin.site.register(Center, CenterAdmin)
