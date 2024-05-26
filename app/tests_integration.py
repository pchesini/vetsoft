from django.test import TestCase
from django.shortcuts import reverse
from app.models import Product


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ProductsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("products_repo"))
        self.assertTemplateUsed(response, "products/repository.html")

    def test_repo_display_all_products(self):
        response = self.client.get(reverse("products_repo"))
        self.assertTemplateUsed(response, "products/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("products_form"))
        self.assertTemplateUsed(response, "products/form.html")

    def test_can_create_product(self):
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            },
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        self.assertEqual(products[0].name, "Producto 1")
        self.assertEqual(products[0].type, "Alimento")
        self.assertEqual(products[0].price, 100)

        self.assertRedirects(response, reverse("products_repo"))

    def test_validation_errors_create_product(self):
        response = self.client.post(
            reverse("products_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un tipo")
        self.assertContains(response, "Por favor ingrese un precio")

    def test_should_response_with_404_status_if_product_doesnt_exists(self):
        response = self.client.get(reverse("products_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_price_zero(self):
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Producto 1",
                "type": "Alimento",
                "price": 0.0,
            },
        )

        self.assertContains(response, "Por favor ingrese un precio mayor a cero")

    def test_validation_invalid_negative_price(self):
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Producto 1",
                "type": "Alimento",
                "price": -100.0,
            },
        )

        self.assertContains(response, "Por favor ingrese un precio mayor a cero")

    def test_validation_invalid_price_input(self):
        response = self.client.post(
            reverse("products_form"),
            data={
                "name": "Producto 1",
                "type": "Alimento",
                "price": "abcd",
            },
        )

        self.assertContains(response, "Por favor ingrese un precio válido")


    def test_edit_product_with_valid_data(self):
        product = Product.objects.create(
            name="Producto 1",
            type= "Alimento",
            price= 100,
        )

        response = self.client.post(
            reverse("products_form"),
            data={
                "id": product.id,
                "name": "Producto 2",
                "type": product.type,
                "price": product.price,
            },
        )

        self.assertEqual(response.status_code, 302)

        editedProduct = Product.objects.get(pk=product.id)
        self.assertEqual(editedProduct.name, "Producto 2")
        self.assertEqual(editedProduct.type, product.type)
        self.assertEqual(editedProduct.price, product.price)
