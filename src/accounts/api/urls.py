from django.urls import path
from . import views


urlpatterns = [
    path('accounts/', views.UserList.as_view(), name="api_accounts"),
    path('account/<int:pk>', views.UserDetail.as_view(), name="api_account_detail"),
]
