from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Child)
admin.site.register(Control)
admin.site.register(Stimulation)
admin.site.register(Message)
