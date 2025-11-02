from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_customer, name="register_customer"),
    path("login/", views.user_login_view, name="user_login"),
    path("admin-login/", views.admin_login_view, name="admin_login"),
    path("logout/", views.logout_view, name="logout"),
]
