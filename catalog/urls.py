from django.urls import path
from . import views


app_name = 'catalog'


urlpatterns = [
    path('main/', views.show_home, name='main'),
    path('contacts/', views.show_contacts, name='contacts')
]