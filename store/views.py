from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.http import require_POST
from decimal import Decimal
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


# ✅ --- Carrito de compras con sesión ---
def cart_view(request):
    """Muestra los productos del carrito"""
    cart = request.session.get('cart', {})
    products = []
    total = Decimal('0.00')

    for product_id, item in cart.items():
        product = get_object_or_404(Product, id=product_id)
        quantity = item.get('quantity', 0)
        subtotal = product.price * quantity
        total += subtotal
        products.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

    context = {
        'products': products,
        'total': total,
    }
    return render(request, 'store/cart.html', context)


# ✅ Agregar producto al carrito
def add_to_cart(request, pk):
    """Agrega un producto al carrito"""
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})

    # Aumenta cantidad si ya está en carrito
    if str(pk) in cart:
        cart[str(pk)]['quantity'] += quantity
    else:
        cart[str(pk)] = {'quantity': quantity}

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f"{product.name} se agregó al carrito correctamente.")
    return redirect('cart')


# ✅ Eliminar producto del carrito
def remove_from_cart(request, pk):
    """Elimina un producto del carrito"""
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
        request.session.modified = True
        messages.info(request, "Producto eliminado del carrito.")
    return redirect('cart')


# ✅ Vaciar todo el carrito
def clear_cart(request):
    """Vacía completamente el carrito"""
    request.session['cart'] = {}
    request.session.modified = True
    messages.info(request, "El carrito ha sido vaciado correctamente.")
    return redirect('cart')


# ✅ Actualizar cantidad (+ o -)
@require_POST
def update_cart(request, pk):
    """Aumenta o disminuye la cantidad de un producto en el carrito"""
    cart = request.session.get('cart', {})
    action = request.POST.get('action')

    if str(pk) in cart:
        if action == 'increase':
            cart[str(pk)]['quantity'] += 1
        elif action == 'decrease' and cart[str(pk)]['quantity'] > 1:
            cart[str(pk)]['quantity'] -= 1
        else:
            # Si llega a 0, lo eliminamos del carrito
            del cart[str(pk)]

        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')
