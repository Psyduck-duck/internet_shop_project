from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import ListView, DetailView, View, TemplateView

from catalog.models import Product


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(DeleteView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


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
