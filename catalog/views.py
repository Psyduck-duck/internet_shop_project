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
    # permission_required = ['catalog.create_product']

    def post(self, request):

        form = ProductForm(request.POST)
        if form.is_valid():
            responce = form.save(commit=False)
            responce.owner = request.user
            responce.save()
            return redirect('catalog:list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'catalog/product_form.html'
    form_class = ProductForm
    success_url = reverse_lazy('catalog:list')
    login_url = reverse_lazy('users:login')

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if request.user.has_perm('catalog.delete_product') or product.owner == request.user:
            form = ProductForm(request.POST)
            if form.is_valid():
                # form.owner = request.user
                # form.save()
                return redirect('catalog:list')

        return HttpResponseForbidden('У вас нет прав для изменения продукта')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_delete.html'
    success_url = reverse_lazy('catalog:list')
    context_object_name = 'product'
    login_url = reverse_lazy('users:login')
    # permission_required = ['catalog.delete_product']

    def post(self, request, pk):

        product = get_object_or_404(Product, id=pk)
        if request.user.has_perm('catalog.delete_product') or product.owner == request.user:
            product.delete()
            return redirect('catalog:list')
        return HttpResponseForbidden('У вас нет прав для удаления продукта')


class UnpublishProductView(LoginRequiredMixin, View):
    model = Product
    template_name = 'catalog/product_unpublish_confirm.html'
    success_url = reverse_lazy('catalog:list')
    login_url = reverse_lazy('users:login')
    context_object_name = 'product'

    def get(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        return render(request, 'catalog/product_unpublish_confirm.html', {'product': product})

    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        if not request.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden('У вас нет прав для снятия / постановки публикации продукта')
        if product.is_published == False:
            product.is_published = True
        else:
            product.is_published = False
        product.save()
        return redirect('catalog:list')


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = reverse_lazy('users:login')
    # permission_required = 'catalog.view_product'


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
