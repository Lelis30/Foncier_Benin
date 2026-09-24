from django.urls import path

from .views import (
    home,
    register,
    login_view,
    logout_view,
    user_dashboard,
    admin_dashboard,
)


urlpatterns = [
    path(
        '',
        home,
        name='home'
    ),

    path(
        'register/',
        register,
        name='register'
    ),

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'dashboard/',
        user_dashboard,
        name='user_dashboard'
    ),

    path(
        'admin-dashboard/',
        admin_dashboard,
        name='admin_dashboard'
    ),
]