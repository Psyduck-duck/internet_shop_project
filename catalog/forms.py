from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data.get('name')
        bad_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']
        if name.lower() in bad_words:
            raise ValidationError(f'Name не может содержать значение {name}')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        bad_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                     'радар']
        if description.lower() in bad_words:
            raise ValidationError(f'Name не может содержать значение {description}')
        return description

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price']
