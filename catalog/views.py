from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden

from .models import Product, Contact
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from .forms import ProductForm

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.models import Product


class ProductHomeListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductsListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'catalog/products_list.html'
    context_object_name = 'products'
    login_url = reverse_lazy('users:login')


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')
    login_url = reverse_lazy('users:login')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')
    login_url = reverse_lazy('users:login')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_delete.html'
    success_url = reverse_lazy('catalog:list')
    context_object_name = 'product'
    login_url = reverse_lazy('users:login')

    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        if request.user.has_perm('catalog.delete_product'):
            product.delete()
            return redirect('catalog:list')
        else:
            return HttpResponseForbidden('У вас нет прав для удаления продукта')


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = reverse_lazy('users:login')
    permission_required = 'catalog.view_product'


class ContactView(View):
    model = Contact
    template_name = 'catalog/contacts.html'
    context_object_name = 'contacts'

    def get(self, request):
        contacts = Contact.objects.all()
        return render(request, 'catalog/contacts.html', {'contacts': contacts})

    def post(self, request):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}! Ваше сообщение принято.')
