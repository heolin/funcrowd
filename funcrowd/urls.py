from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path


urlpatterns = []
urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    path('admin/', admin.site.urls),
]
