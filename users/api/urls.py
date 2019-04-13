from django.urls import path

from users.api.views.auth import (
    EndWorkerView,
    EndWorkerLoginView,
    EndWorkerLogoutView,
    EndWorkerRegistrationView,
)
from users.api.views.mturk import (
    MturkRegisterLoginView
)
from users.api.views.storage import (
    EndWorkerStorageView, EndWorkerStorageBatchView
)


urlpatterns = [
    path('login', EndWorkerLoginView.as_view(), name='login_end_worker'),
    path('mturk', MturkRegisterLoginView.as_view(), name='register_mturk'),
    path('register', EndWorkerRegistrationView.as_view(), name='register_end_worker'),
    path('current', EndWorkerView.as_view(), name='current_end_worker'),
    path('logout', EndWorkerLogoutView.as_view(), name='current_end_worker'),
    path('storage/<str:key>', EndWorkerStorageView.as_view(), name='end_worker_storage'),
    path('storage', EndWorkerStorageBatchView.as_view(), name='end_worker_storage_batch'),
]
