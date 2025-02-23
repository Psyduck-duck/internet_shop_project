from .models import Product


class ProductService:

    @staticmethod
    def get_only_category_products(category_id):
        """ метод для получения продуктов определенной категории """

        category_products = Product.objects.filter(category_id=category_id)
        if not category_products.exists():
            return None
        return category_products
