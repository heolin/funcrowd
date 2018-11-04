from django.urls import path, include


urlpatterns = [
    path('users/', include('users.api.urls')),
]
