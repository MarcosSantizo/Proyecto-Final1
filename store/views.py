from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Product, Category

# ✅ Vista para listar productos (panel de administración)
class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'


# ✅ Crear un producto
class ProductCreateView(CreateView):
    model = Product
    template_name = 'store/product_form.html'
    fields = ['name', 'description', 'price', 'stock', 'category', 'sku', 'image']
    success_url = reverse_lazy('product_list')


# ✅ Detalle del producto (página pública)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


# ✅ Actualizar producto
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'store/product_form.html'
    fields = ['name', 'description', 'price', 'stock', 'category', 'sku', 'image']
    success_url = reverse_lazy('product_list')


# ✅ Eliminar producto
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


# ✅ Página principal de la tienda (categorías)
class StoreCategoryListView(ListView):
    model = Category
    template_name = 'store/store_home.html'
    context_object_name = 'categories'


# ✅ Productos por categoría
class CategoryProductListView(ListView):
    model = Product
    template_name = 'store/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_id = self.kwargs['pk']
        return Product.objects.filter(category_id=category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['pk'])
        return context


# ✅ Agregar producto al carrito (por ahora redirige al carrito vacío)
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Aquí luego guardaremos en sesión
    return redirect('cart')


# ✅ Carrito de compras vacío (por ahora)
def cart_view(request):
    return render(request, 'store/cart.html', {})
