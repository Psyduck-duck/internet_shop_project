from .models import Product


class ProductService:

    @staticmethod
    def get_only_group_products(group_id):
        """ метод для получения продуктов определенной категории """

        group_products = Product.objects.filter(group_id=group_id)
        if not group_products.exists():
            return None
        return group_products
