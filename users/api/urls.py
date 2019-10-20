from django.urls import path

from users.api.views.auth import (
    EndWorkerView,
    EndWorkerLoginView,
    EndWorkerLogoutView,
    EndWorkerRegistrationView,
    EndWorkerEmailInfoView,
    EndWorkerUsernameInfoView,
    EndWorkerStatusView
)
from users.api.views.mturk import (
    MturkRegisterLoginView
)
from users.api.views.storage import (
    EndWorkerStorageView, EndWorkerStorageBatchView
)


urlpatterns = [
    path('check/email', EndWorkerEmailInfoView.as_view(), name='check_email_end_worker'),
    path('check/username', EndWorkerUsernameInfoView.as_view(), name='check_username_end_worker'),
    path('login', EndWorkerLoginView.as_view(), name='login_end_worker'),
    path('mturk', MturkRegisterLoginView.as_view(), name='register_mturk'),
    path('register', EndWorkerRegistrationView.as_view(), name='register_end_worker'),
    path('current', EndWorkerView.as_view(), name='current_end_worker'),
    path('status', EndWorkerStatusView.as_view(), name='end_worker_status'),
    path('logout', EndWorkerLogoutView.as_view(), name='end_worker_logout'),
    path('storage/<str:key>', EndWorkerStorageView.as_view(), name='end_worker_storage'),
    path('storage', EndWorkerStorageBatchView.as_view(), name='end_worker_storage_batch'),
]
