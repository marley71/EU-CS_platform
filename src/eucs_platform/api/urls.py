from django.urls import path, include

from .views import APIRoot
from accounts.api.urls import urlpatterns as accounts_api_urlpatterns
from organisations.api.urls import urlpatterns as organisations_api_urlpatterns
from projects.api.urls import urlpatterns as projects_api_urlpatterns
from resources.api.urls import urlpatterns as resources_api_urlpatterns

urlpatterns = [
    path('', APIRoot.as_view(), name='api-root'),
    *accounts_api_urlpatterns,
    *organisations_api_urlpatterns,
    *projects_api_urlpatterns,
    *resources_api_urlpatterns,
]
