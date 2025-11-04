from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from decimal import Decimal
from .models import Product, Category


# ✅ --- Panel protegido para admin/staff ---
@login_required
@staff_member_required
def admin_dashboard(request):
    """Panel principal solo para staff o superusuarios"""
    return render(request, 'store/admin_dashboard.html')


# ✅ --- CRUD de Categorías ---
@method_decorator(staff_member_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'store/category_list.html'
    context_object_name = 'categories'


@method_decorator(staff_member_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    template_name = 'store/category_form.html'
    fields = ['name', 'description', 'image']
    success_url = reverse_lazy('category_list')


@method_decorator(staff_member_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'store/category_form.html'
    fields = ['name', 'description', 'image']
    success_url = reverse_lazy('category_list')


@method_decorator(staff_member_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'store/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


# ✅ --- CRUD de Productos ---
@method_decorator(staff_member_required, name='dispatch')
class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'


@method_decorator(staff_member_required, name='dispatch')
class ProductCreateView(CreateView):
    model = Product
    template_name = 'store/product_form.html'
    fields = ['name', 'description', 'price', 'stock', 'category', 'sku', 'image']
    success_url = reverse_lazy('product_list')


@method_decorator(staff_member_required, name='dispatch')
class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'store/product_form.html'
    fields = ['name', 'description', 'price', 'stock', 'category', 'sku', 'image']
    success_url = reverse_lazy('product_list')


@method_decorator(staff_member_required, name='dispatch')
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'store/product_confirm_delete.html'
    success_url = reverse_lazy('product_list')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store/product_detail.html'
    context_object_name = 'product'


# ✅ --- Tienda pública ---
class StoreCategoryListView(ListView):
    model = Category
    template_name = 'store/store_home.html'
    context_object_name = 'categories'


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


# ✅ --- Carrito de compras ---
def cart_view(request):
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

    context = {'products': products, 'total': total}
    return render(request, 'store/cart.html', context)


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    quantity = int(request.POST.get('quantity', 1))
    cart = request.session.get('cart', {})

    if str(pk) in cart:
        cart[str(pk)]['quantity'] += quantity
    else:
        cart[str(pk)] = {'quantity': quantity}

    request.session['cart'] = cart
    request.session.modified = True
    messages.success(request, f"{product.name} se agregó al carrito correctamente.")
    return redirect('cart')


def remove_from_cart(request, pk):
    cart = request.session.get('cart', {})
    if str(pk) in cart:
        del cart[str(pk)]
        request.session['cart'] = cart
        request.session.modified = True
        messages.info(request, "Producto eliminado del carrito.")
    return redirect('cart')


def clear_cart(request):
    request.session['cart'] = {}
    request.session.modified = True
    messages.info(request, "El carrito ha sido vaciado correctamente.")
    return redirect('cart')


@require_POST
def update_cart(request, pk):
    cart = request.session.get('cart', {})
    action = request.POST.get('action')

    if str(pk) in cart:
        if action == 'increase':
            cart[str(pk)]['quantity'] += 1
        elif action == 'decrease' and cart[str(pk)]['quantity'] > 1:
            cart[str(pk)]['quantity'] -= 1
        else:
            del cart[str(pk)]
        request.session['cart'] = cart
        request.session.modified = True

    return redirect('cart')


# ✅ --- Finalizar compra ---
@login_required
def checkout_view(request):
    """Finaliza la compra y limpia el carrito"""
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('cart')

    # Simula la compra y limpia el carrito
    request.session['cart'] = {}
    request.session.modified = True

    context = {
        'user_name': request.user.first_name or request.user.username,
    }

    return render(request, 'store/checkout_success.html', context)


# ✅ --- Buscador global ---
def product_search(request):
    """Busca productos por nombre o descripción"""
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'store/product_search_results.html', context)
