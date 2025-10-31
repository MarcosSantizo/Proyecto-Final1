from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
    StoreCategoryListView,
    CategoryProductListView,
    add_to_cart,
    cart_view,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('producto/nuevo/', ProductCreateView.as_view(), name='product_create'),
    path('producto/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('producto/<int:pk>/editar/', ProductUpdateView.as_view(), name='product_update'),
    path('producto/<int:pk>/eliminar/', ProductDeleteView.as_view(), name='product_delete'),

    # 🏬 Tienda y categorías
    path('tienda/', StoreCategoryListView.as_view(), name='store_home'),
    path('tienda/categoria/<int:pk>/', CategoryProductListView.as_view(), name='category_products'),

    # 🛒 Carrito
    path('carrito/', cart_view, name='cart'),
    path('carrito/agregar/<int:pk>/', add_to_cart, name='add_to_cart'),
]
