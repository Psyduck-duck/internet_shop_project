from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=150, verbose_name='Название группы')
    description = models.TextField(verbose_name='Описание группы')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']


class Product(models.Model):

    name = models.CharField(max_length=150, verbose_name='имя')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to='photos/', verbose_name='фотография')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='название группы')
    price = models.IntegerField(verbose_name='цена')
    create_date = models.DateField(auto_now=True, verbose_name='дата создания')
    lust_change_date = models.DateField(auto_now_add=True, verbose_name='дата последнего изменения')

    def __str__(self):
        return f'{self.name} ({self.category}), {self.price} руб.'

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        ordering = ['name']
