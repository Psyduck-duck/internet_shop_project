from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm
from django.views.generic.edit import CreateView



class CustomLoginView(LoginView):
    template_name = 'login.html'


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('catalog:home')
