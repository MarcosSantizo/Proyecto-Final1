from django.urls import path
from . import views

urlpatterns = [
    path('', views.StoreCategoryListView.as_view(), name='store_home'),
    path('categoria/<int:pk>/', views.CategoryProductListView.as_view(), name='category_products'),
    path('producto/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Carrito
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('update-cart/<int:pk>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout_view, name='checkout'),

    # Buscador
    path('buscar/', views.product_search, name='product_search'),

    # CRUD Categorías y Productos
    path('categorias/', views.CategoryListView.as_view(), name='category_list'),
    path('categorias/nueva/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categorias/editar/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categorias/eliminar/<int:pk>/', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('productos/', views.ProductListView.as_view(), name='product_list'),
    path('productos/nuevo/', views.ProductCreateView.as_view(), name='product_create'),
    path('productos/editar/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('productos/eliminar/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
]
