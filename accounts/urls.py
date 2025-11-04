from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.user_login_view, name="user_login"),             # Login clientes
    path("admin-login/", views.admin_login_view, name="admin_login"),     # Login admin
    path("register/", views.register_customer, name="register_customer"), # Registro
    path("logout/", views.logout_view, name="logout"),                    # Logout
]
