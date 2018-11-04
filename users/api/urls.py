from django.urls import path

from users.api.views.auth import (
    EndWorkerView,
    EndWorkerLoginView,
    EndWorkerLogoutView,
    EndWorkerRegistrationView,
)

urlpatterns = [
    path('login', EndWorkerLoginView.as_view(), name='login_end_worker'),
    path('register', EndWorkerRegistrationView.as_view(), name='register_end_worker'),
    path('current', EndWorkerView.as_view(), name='current_end_worker'),
    path('logout', EndWorkerLogoutView.as_view(), name='current_end_worker'),
]
