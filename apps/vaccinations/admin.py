from django.contrib import admin
from .models import *
from suit.admin import SortableModelAdmin


class VaccineAdmin(SortableModelAdmin):
    filter_horizontal = ('related_diseases', 'related_centers')
    sortable = 'order'

admin.site.register(Disease)
admin.site.register(Vaccine, VaccineAdmin)
