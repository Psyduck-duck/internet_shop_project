from django.core.exceptions import PermissionDenied
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

from .models import Product, Contact, Category
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from .forms import ProductForm
from .services import ProductService

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

    def get_queryset(self):
        queryset = cache.get('my_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('my_quaryset', queryset, 60*15)
        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


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

    def get_form_class(self):
        user = self.request.user
        if user.has_perm('catalog.update_product') or self.object.owner == user:
            return ProductForm

        raise PermissionDenied('У вас нет прав для изменения продукта')


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


@method_decorator(cache_page(60*15), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    login_url = reverse_lazy('users:login')
    # permission_required = 'catalog.view_product'


class CategoryProductsListView(DeleteView):
    model = Category
    template_name = 'catalog/group_product_list.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        group_id = self.object.id
        context['products'] = ProductService.get_only_category_products(group_id)
        return context


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
