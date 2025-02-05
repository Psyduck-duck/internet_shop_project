from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Название товара'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Описание товара'})
        self.fields['category'].widget.attrs.update({'class': 'form-control'})
        self.fields['price'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Цена'})

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

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price']
