from django.urls import path
from apps.accounts.views import login_view, logout_view, register_view
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/login/', login_view.LoginView.as_view(), name='login'),
    path('auth/logout/', logout_view.LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', register_view.RegisterView.as_view(), name='register'),
]
