from django.conf.urls import url, include, patterns
from django.contrib import admin
from django.conf import settings
from apps.control.views import IndexView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('apps.centers.urls')),
    url(r'^api/', include('apps.control.urls')),
    url(r'^api/', include('apps.vaccinations.urls')),
    url(r'^$', IndexView.as_view(), name='index'),

]
if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.STATIC_ROOT}),
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT}), )
