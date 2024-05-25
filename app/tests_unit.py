from django.test import TestCase
from app.models import Product


class ProductModelTest(TestCase):
    def test_can_create_and_get_product(self):
        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            }
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        self.assertEqual(products[0].name, "Producto 1")
        self.assertEqual(products[0].type, "Alimento")
        self.assertEqual(products[0].price, 100.0)

    def test_can_update_product(self):
        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            }
        )
        
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 100.0)

        product.update_product({"price": 200.0})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 200.0)

    def test_update_product_with_error(self):
        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            }
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 100.0)

        product.update_product({"price": ""})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 100.0)
