from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_swagger.views import get_swagger_view
from django.urls import path, include

schema_view = get_swagger_view(title='FunCrowd API')

urlpatterns = []
urlpatterns += staticfiles_urlpatterns()
urlpatterns += [
    path('', schema_view),
    path('admin/', admin.site.urls),
    path('api/v1/', include('tasks.api.urls')),
    path('api/v1/', include('users.urls')),
]