from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login, name="user_login"),
    path("admin-login/", views.admin_login, name="admin_login"),
    path("logout/", views.logout_view, name="logout_view"),
    path("register/", views.register_customer, name="register_customer"),
]
