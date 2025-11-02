from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# ✅ --- Login de usuario normal ---
def user_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                messages.warning(request, "Por favor, usa el login de administrador.")
                return redirect("admin_login")

            login(request, user)
            messages.success(request, f"Bienvenido {user.username}")
            return redirect("/")  # 👈 redirige a la tienda

        messages.error(request, "Usuario o contraseña incorrectos.")
        return redirect("user_login")

    return render(request, "accounts/login.html")


# ✅ --- Login de administrador ---
def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect("/admin-dashboard/")  # 👈 Panel admin
            else:
                messages.error(request, "No tienes permisos de administrador.")
                return redirect("user_login")

        messages.error(request, "Usuario o contraseña incorrectos.")
        return redirect("admin_login")

    return render(request, "accounts/admin_login.html")


# ✅ --- Registro de cliente ---
def register_customer(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("register_customer")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya existe.")
            return redirect("register_customer")

        user = User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Cuenta creada con éxito. Inicia sesión.")
        return redirect("user_login")

    return render(request, "accounts/register.html")


# ✅ --- Logout general ---
@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect("/")
