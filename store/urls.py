from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductDetailView,
    ProductUpdateView,
    ClientProductListView,
)

urlpatterns = [
    # Rutas de administración
    path('', ProductListView.as_view(), name='product_list'),
    path('producto/nuevo/', ProductCreateView.as_view(), name='product_create'),
    path('producto/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('producto/<int:pk>/editar/', ProductUpdateView.as_view(), name='product_update'),

    # Pestaña para clientes
    path('tienda/', ClientProductListView.as_view(), name='client_product_list'),
]
