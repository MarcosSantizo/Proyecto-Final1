from django.urls import path
from .views import (
    ProductListView, ProductCreateView, ProductDetailView,
    ProductUpdateView, ProductDeleteView,
    StoreCategoryListView, CategoryProductListView,
    cart_view, add_to_cart, remove_from_cart, clear_cart, update_cart,
    admin_dashboard
)

urlpatterns = [
    path('', admin_dashboard, name='admin_dashboard'),

    # --- Tienda pública ---
    path('tienda/', StoreCategoryListView.as_view(), name='store_home'),
    path('categoria/<int:pk>/', CategoryProductListView.as_view(), name='category_products'),

    # --- Productos (panel) ---
    path('productos/', ProductListView.as_view(), name='product_list'),
    path('productos/nuevo/', ProductCreateView.as_view(), name='product_create'),
    path('productos/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('productos/<int:pk>/editar/', ProductUpdateView.as_view(), name='product_update'),
    path('productos/<int:pk>/eliminar/', ProductDeleteView.as_view(), name='product_delete'),

    # --- Carrito ---
    path('carrito/', cart_view, name='cart'),
    path('carrito/agregar/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('carrito/eliminar/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('carrito/vaciar/', clear_cart, name='clear_cart'),
    path('carrito/actualizar/<int:pk>/', update_cart, name='update_cart'),
]
