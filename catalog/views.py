from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact


def show_home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})


def show_contacts(request):
    contacts = Contact.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        return HttpResponse(f'Спасибо, {name}! Ваше сообщение принято.')
    return render(request, 'catalog/contacts.html', {'contacts': contacts})


def show_product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'product': product
    }
    return render(request, 'catalog/product_detail.html', context)
