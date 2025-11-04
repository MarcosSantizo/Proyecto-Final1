from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


# ✅ Login de cliente (usuario normal)
def user_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_staff:  # Solo clientes
                login(request, user)
                messages.success(request, f"Bienvenido, {user.first_name or user.username} 👋")
                return redirect("store_home")
            else:
                messages.error(request, "Usa el acceso de administrador para entrar al panel.")
                return redirect("admin_login")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
            return redirect("user_login")

    return render(request, "accounts/user_login.html")


# ✅ Login de administrador (staff)
def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f"Bienvenido al panel, {user.username}")
            return redirect("/admin/")
        else:
            messages.error(request, "Credenciales inválidas o sin permisos de administrador.")
            return redirect("admin_login")

    return render(request, "accounts/admin_login.html")

def register_customer(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        first_name = request.POST.get("first_name")

        if not first_name:
            messages.error(request, "El nombre es obligatorio.")
            return redirect("register_customer")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return redirect("register_customer")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect("register_customer")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name
        )
        user.save()

        messages.success(request, "Cuenta creada exitosamente. Inicia sesión.")
        return redirect("user_login")

    return render(request, "accounts/register.html")


# ✅ Logout general
def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect("store_home")
