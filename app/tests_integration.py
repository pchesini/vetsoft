from django.test import TestCase
from django.shortcuts import reverse
from app.models import Product, Client, Vet, Provider, Medi


class HomePageTest(TestCase):
    def test_use_home_template(self):
        response = self.client.get(reverse("home"))
        self.assertTemplateUsed(response, "home.html")


class ClientsTest(TestCase):
    def test_repo_use_repo_template(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_repo_display_all_clients(self):
        response = self.client.get(reverse("clients_repo"))
        self.assertTemplateUsed(response, "clients/repository.html")

    def test_form_use_form_template(self):
        response = self.client.get(reverse("clients_form"))
        self.assertTemplateUsed(response, "clients/form.html")

    def test_can_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

        self.assertRedirects(response, reverse("clients_repo"))

    def test_validation_errors_create_client(self):
        response = self.client.post(
            reverse("clients_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un teléfono")
        self.assertContains(response, "Por favor ingrese un email")

    def test_should_response_with_404_status_if_client_doesnt_exists(self):
        response = self.client.get(reverse("clients_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_validation_invalid_email(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75",
            },
        )

        self.assertContains(response, "Por favor ingrese un email valido")

    def test_validation_invalid_email_wrong_ending(self):
        response = self.client.post(
            reverse("clients_form"),
            data={
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@yahoo.com",
            },
        )

        self.assertContains(response, "Por favor ingrese un email terminado en @vetsoft.com")

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@vetsoft.com",
        )

        response = self.client.post(
            reverse("clients_form"),
            data={
                "id": client.id,
                "name": "Guido Carrillo",
            },
        )

        # redirect after post
        self.assertEqual(response.status_code, 302)

        editedClient = Client.objects.get(pk=client.id)
        self.assertEqual(editedClient.name, "Guido Carrillo")
        self.assertEqual(editedClient.phone, client.phone)
        self.assertEqual(editedClient.address, client.address)
        self.assertEqual(editedClient.email, client.email)

###TEST MEDICINE###
class MedicineTest(TestCase):

    def test_validation_invalid_dose_below_range(self):
        # Enviamos una solicitud POST al formulario de creación de medicamentos con una dosis inválida (fuera del rango permitido, menor que 1)
        response = self.client.post(
            reverse("medi_form"),
            data={
                "name": "Paracetamol",
                "description": "Analgesico",
                "dose": "0",  # Dosis fuera del rango permitido (menor que 1)
            },
        )
        self.assertContains(response, "Por favor ingrese una dosis entre 1 y 10")


    def test_validation_invalid_dose_above_range(self):
        # Enviamos una solicitud POST al formulario de creación de medicamentos con una dosis inválida (fuera del rango permitido, mayor que 10)
        response = self.client.post(
            reverse("medi_form"),
            data={
                "name": "Paracetamol",
                "description": "Analgesico",
                "dose": 15,  # Dosis fuera del rango permitido (mayor que 10)
            },
        )

        self.assertContains(response, "Por favor ingrese una dosis entre 1 y 10")

    def test_edit_medicine_with_valid_data(self):
        # Creamos un medicamento en la base de datos
        medicine = Medi.objects.create(
            name="Paracetamol",
            description="Analgesico",
            dose=5,
        )

        # Enviamos una solicitud POST para editar el medicamento
        response = self.client.post(
            reverse("medi_form"),
            data={
                "id": medicine.id,
                "dose": "9",  # Nueva dosis
            },
        )

        # Verificamos que la solicitud redirija correctamente
        self.assertEqual(response.status_code, 302)

        # Obtenemos el objeto de medicamento actualizado de la base de datos
        edited_medicine = Medi.objects.get(pk=medicine.id)

        # Verificamos que la dosis se haya actualizado correctamente
        self.assertEqual(edited_medicine.name, medicine.name)
        self.assertEqual(edited_medicine.description, medicine.description)
        self.assertEqual(edited_medicine.dose, 9)  # Verificamos la nueva dosis


class VetsTest(TestCase):
    def test_vet_table_shows_specialty(self):

        self.client.post(
            reverse("vets_form"),
            data={
                "name": "Mariano Navone",
                "phone": "2219870789",
                "email": "lanavoneta@gmail.com",
                "specialty": Vet.VetSpecialties.ONCOLOGIA
            },
        )

        vet = Vet.objects.all()[0]  #Creo un vet y lo recupero


        response = self.client.get(reverse("vets_repo"))
        self.assertTemplateUsed(response, "vets/repository.html")
        self.assertContains(response, '<table')
        self.assertContains(response, '<th>Especialidad') #Verifico que la tabla tenga especialidad
        self.assertContains(response, vet.specialty) #Verifico que la especialidad se muestre

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



class ProviderIntegrationTest(TestCase):
    def test_can_create_provider(self):
        response = self.client.post(
            reverse("provider_form"),
            data={
                "name": "Proveedor Ejemplo",
                "email": "proveedor@ejemplo.com",
                "address": "Calle Falsa 123",
            },
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Proveedor Ejemplo")
        self.assertEqual(providers[0].email, "proveedor@ejemplo.com")
        self.assertEqual(providers[0].address, "Calle Falsa 123")

        self.assertRedirects(response, reverse("provider_repo"))

    def test_validation_errors_create_provider(self):
        response = self.client.post(
            reverse("provider_form"),
            data={},
        )

        self.assertContains(response, "Por favor ingrese un nombre")
        self.assertContains(response, "Por favor ingrese un email")
        self.assertContains(response, "Por favor ingrese una dirección")

    def test_should_response_with_404_status_if_provider_doesnt_exists(self):
        response = self.client.get(reverse("provider_edit", kwargs={"id": 100}))
        self.assertEqual(response.status_code, 404)

    def test_edit_provider_with_valid_data(self):
        provider = Provider.objects.create(
            name="Proveedor Ejemplo",
            email="proveedor@ejemplo.com",
            address="Calle Falsa 123",
        )

        response = self.client.post(
            reverse("provider_form"),
            data={
                "id": provider.id,
                "name": "Nuevo Proveedor",
            },
        )

        self.assertEqual(response.status_code, 302)

        editedProvider = Provider.objects.get(pk=provider.id)
        self.assertEqual(editedProvider.name, "Nuevo Proveedor")
        self.assertEqual(editedProvider.email, provider.email)
        self.assertEqual(editedProvider.address, provider.address)
