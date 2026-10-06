from django.urls import path
from accounts.views import login_view, logout_view, register_view

urlpatterns = [
    path('auth/login/', login_view.LoginView.as_view(), name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/register/', register_view, name='register'),
]
