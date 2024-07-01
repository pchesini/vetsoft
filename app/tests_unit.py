from django.forms import ValidationError
from django.test import TestCase

from app.models import Client, Medi, Product, Provider, Vet, validate_client


class ClientModelTest(TestCase):
    """Pruebas para el modelo Client."""

    def test_can_create_and_get_client(self):
        """Verifica si se puede crear y obtener un cliente."""
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, 54221555232)
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

    def test_can_update_client(self):
        """Verifica si se puede actualizar un cliente."""

        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, 54221555232)

        client.update_client({"phone": "54221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, 54221555233)

    def test_update_client_with_error(self):
        """Verifica si se puede actualizar un cliente con un error."""

        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "54221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, 54221555232)

        client.update_client({"phone": "54221555232"})

        client_updated = Client.objects.get(pk=1)


        self.assertEqual(client_updated.phone, 54221555232)

    def test_name_validation_only_letters_and_spaces(self):
        # Intenta guardar un cliente con un nombre válido
        valid_client_data = {
            "name": "Juan Sebastian Veron",
            "phone": 54221555232,
            "address": "13 y 44",
            "email": "brujita75@vetsoft.com",
        }

        is_saved, errors = Client.save_client(valid_client_data)  # Aquí guardamos el cliente válido


        # Verifica que el cliente se haya guardado correctamente
        self.assertTrue(is_saved)
        self.assertIsNone(errors)

        # Intenta guardar un cliente con un nombre inválido
        invalid_client_data = {
            "name": "Juan123",
            "phone": 54221555232,
            "address": "13 y 44",
            "email": "brujita75@vetsoft.com",
        }
        is_saved, errors = Client.save_client(invalid_client_data)

        # Verifica que el cliente no se haya guardado debido a la validación
        self.assertFalse(is_saved)
        self.assertIn("name", errors)

    def test_name_validation_with_special_characters(self):
    # Intenta guardar un cliente con un nombre que contiene caracteres especiales
        special_characters_name = "Juan&* Sebastian Veron"
        client_data = {
        "name": special_characters_name,
        "phone": 54221555232,
        "address": "13 y 44",
        "email": "brujita75@vetsoft.com",
    }

    # Intenta guardar el cliente
        is_saved, errors = Client.save_client(client_data)

    # Verifica que el cliente no se haya guardado debido a la presencia de caracteres especiales
        self.assertFalse(is_saved)
        self.assertIn("name", errors)

    def test_can_not_create_without_vetsoft_email(self):

        is_saved, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": 54221555232,
                "address": "13 y 44",
                "email": "brujita75@yahoo.com",
            }
        )
        self.assertFalse(is_saved)
        self.assertIn("email", errors)
        self.assertIn("Por favor ingrese un email terminado en @vetsoft.com", errors["email"])

    def test_can_not_create_with_invalid_email(self):

        is_saved, errors = Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": 54221555232,
                "address": "13 y 44",
                "email": "@vetsoft.com",
            }
        )
        self.assertFalse(is_saved)
        self.assertIn("email", errors)
        self.assertIn("Por favor ingrese un email valido", errors["email"])


    def test_phone_number_must_be_numeric(self):
        """Verifica que el número de teléfono sea numérico."""

        # Prueba con un teléfono numérico válido
        data = {
            "name": "Juan Sebastian Veron",
            "phone": "54221555232",
            "address": "13 y 44",
            "email": "brujita75@vetsoft.com",
        }
        errors = validate_client(data)
        self.assertEqual(errors, {})

        # Prueba con un teléfono no numérico
        data = {
            "name": "Juan Sebastian Veron",
            "phone": "54221A555232",
            "address": "13 y 44",
            "email": "brujita75@vetsoft.com",
        }
        errors = validate_client(data)
        self.assertEqual(errors, {"phone": "El teléfono debe ser numérico"})

        # Prueba con un teléfono que contiene espacios
        data = {
            "name": "Juan Sebastian Veron",
            "phone": "54221 555 232",
            "address": "13 y 44",
            "email": "brujita75@vetsoft.com",
        }
        errors = validate_client(data)
        self.assertEqual(errors, {"phone": "El teléfono debe ser numérico"})

class MedicineModelTest(TestCase):
    """Pruebas para el modelo Medi (Medicine)."""
    def test_can_create_and_get_medicine(self):
        """Verifica si se puede crear y obtener un medicamento."""

        Medi.save_medi(
            {
                "name": "Paracetamol",
                "description": "Analgesico",
                "dose": "5",
            },
        )
        medicines = Medi.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Paracetamol")
        self.assertEqual(medicines[0].description, "Analgesico")
        self.assertEqual(medicines[0].dose, 5)

    def test_can_update_medicine(self):
        """Verifica si se puede actualizar un medicamento."""

        Medi.save_medi(
            {
                "name": "Paracetamol",
                "description": "Analgesico",
                "dose": "5",
            },
        )
        medicine = Medi.objects.get(pk=1)

        self.assertEqual(medicine.dose, 5)

        medicine.update_medi({"dose": "9"})  # Nueva dosis

        medicine_updated = Medi.objects.get(pk=1)

        self.assertEqual(medicine_updated.dose, 9)

    def test_update_medicine_with_error(self):
        """Verifica si se puede actualizar un medicamento con un error."""

        Medi.save_medi(
            {
                "name": "Paracetamol",
                "description": "Analgesico",
                "dose": "5",
            },
        )
        medicine = Medi.objects.get(pk=1)

        self.assertEqual(medicine.dose, 5)

        # Intentamos actualizar la dosis con un valor inválido en este caso vacio
        medicine.update_medi({"dose": ""})

        # El valor de la dosis no debe haber cambiado
        medicine_updated = Medi.objects.get(pk=1)
        self.assertEqual(medicine_updated.dose, 5, "La dosis no debe cambiar si se proporciona un valor de dosis inválido")

class VetModelTest(TestCase):
    """Pruebas para el modelo Vet."""

    def test_can_create_and_get_vet(self):
        """Verifica si se puede crear y obtener un veterinario."""

        Vet.save_vet(
            {
                "name": "Mariano Navone",
                "phone": "2219870789",
                "email": "lanavoneta@gmail.com",
                "specialty": Vet.VetSpecialties.SIN_ESPECIALIDAD,
            },
        )
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)

        self.assertEqual(vets[0].name, "Mariano Navone")
        self.assertEqual(vets[0].phone, "2219870789")
        self.assertEqual(vets[0].email, "lanavoneta@gmail.com")
        self.assertEqual(vets[0].specialty, Vet.VetSpecialties.SIN_ESPECIALIDAD)

    def test_can_update_vet_specialty(self):
        """Verifica si se puede actualizar la especialidad de un veterinario."""

        Vet.save_vet(
            {
                "name": "Mariano Navone",
                "phone": "2219870789",
                "email": "lanavoneta@gmail.com",
                "specialty": Vet.VetSpecialties.SIN_ESPECIALIDAD,
            },
        )
        vet = Vet.objects.get(pk=1)

        self.assertEqual(vet.specialty, Vet.VetSpecialties.SIN_ESPECIALIDAD)

        vet.update_vet({"specialty": Vet.VetSpecialties.CARDIOLOGIA})

        vet_updated = Vet.objects.get(pk=1)

        self.assertEqual(vet_updated.specialty, Vet.VetSpecialties.CARDIOLOGIA)

    def test_specialty_choices(self):
        """Verifica las opciones de especialidad disponibles."""

        expected_choices = [
            ("Sin especialidad", "Sin especialidad"),
            ("Cardiología", "Cardiología"),
            ("Medicina interna de pequeños animales", "Medicina interna de pequeños animales"),
            ("Medicina interna de grandes animales", "Medicina interna de grandes animales"),
            ("Neurología", "Neurología"),
            ("Oncología", "Oncología"),
            ("Nutrición", "Nutrición"),
        ]

        self.assertEqual(Vet.VetSpecialties.choices, expected_choices)

class ProductModelTest(TestCase):
    """Pruebas para el modelo Product."""

    def test_can_create_and_get_product(self):
        """Verifica si se puede crear y obtener un producto."""

        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            },
        )
        products = Product.objects.all()
        self.assertEqual(len(products), 1)

        self.assertEqual(products[0].name, "Producto 1")
        self.assertEqual(products[0].type, "Alimento")
        self.assertEqual(products[0].price, 100.0)

    def test_can_update_product(self):
        """Verifica si se puede actualizar un producto."""

        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            },
        )

        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 100.0)

        product.update_product({"price": 200.0})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 200.0)

    def test_update_product_with_empty_price(self):
        """Verifica si se puede actualizar un producto con un precio vacío."""

        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            },
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 100.0)

        product.update_product({"price": ""})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 100.0)

    def test_update_product_with_negative_price(self):
        """Verifica si se puede actualizar un producto con un precio negativo."""

        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            },
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 100.0)

        product.update_product({"price": -100.0})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 100.0)

    def test_update_product_with_price_zero(self):
        """Verifica si se puede actualizar un producto con un precio de cero."""

        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            },
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 100.0)

        product.update_product({"price": 0.0})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 100.0)



class ProviderModelTest(TestCase):
    """Pruebas para el modelo Provider."""

    def test_can_create_and_get_provider(self):
        """Verifica si se puede crear y obtener un proveedor."""

        Provider.objects.create(
            name="Proveedor Ejemplo",
            email="proveedor@ejemplo.com",
            address="13 y 32",
        )
        providers = Provider.objects.all()
        self.assertEqual(len(providers), 1)

        self.assertEqual(providers[0].name, "Proveedor Ejemplo")
        self.assertEqual(providers[0].email, "proveedor@ejemplo.com")
        self.assertEqual(providers[0].address, "13 y 32")
