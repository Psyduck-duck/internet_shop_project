from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Add test products to the db'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        call_command('loaddata', 'catalog_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))

