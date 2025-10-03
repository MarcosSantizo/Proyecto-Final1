from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Product

# Listado de productos para administración
class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'

# Detalle de producto
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'

# Crear nuevo producto
class ProductCreateView(CreateView):
    model = Product
    template_name = 'store/product_form.html'
    fields = ['name', 'category', 'price', 'stock', 'description', 'image']
    success_url = reverse_lazy('product_list')

# Editar producto existente
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'store/product_form.html'
    fields = ['name', 'category', 'price', 'stock', 'description', 'image']
    success_url = reverse_lazy('product_list')

# Listado de productos para clientes
class ClientProductListView(ListView):
    model = Product
    template_name = 'store/client_product_list.html'  # template exclusivo para clientes
    context_object_name = 'products'
