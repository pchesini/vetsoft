from django.test import TestCase
from app.models import Product, Client, Vet, Provider, Medi


class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@vetsoft.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": "221555233"})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555233")

    def test_update_client_with_error(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@vetsoft.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

    def test_can_not_create_with_invalid_email(self):

        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@yahoo.com",
            }
        )
        clients = Client.objects.all()
        self.assertNotEqual(len(clients), 1)



class MedicineModelTest(TestCase):
    #verifica si se puede crear un nuevo medicamento y si se guarda en la bd
    def test_can_create_and_get_medicine(self):
        Medi.save_medi(
            {
                "name": "Paracetamol",
                "description": "Analgesico",
                "dose": "5",
            }
        )
        medicines = Medi.objects.all()
        self.assertEqual(len(medicines), 1)

        self.assertEqual(medicines[0].name, "Paracetamol")
        self.assertEqual(medicines[0].description, "Analgesico")
        self.assertEqual(medicines[0].dose, 5)

    #Esta prueba comprueba si se puede actualizar la dosis de un medicamento
    def test_can_update_medicine(self):
        Medi.save_medi(
            {
                "name": "Paracetamol",
                "description": "Analgesico",
                "dose": "5",
            }
        )
        medicine = Medi.objects.get(pk=1)

        self.assertEqual(medicine.dose, 5)

        medicine.update_medi({"dose": "9"})  # Nueva dosis

        medicine_updated = Medi.objects.get(pk=1)

        self.assertEqual(medicine_updated.dose, 9)

    def test_update_medicine_with_error(self):
        Medi.save_medi(
            {
                "name": "Paracetamol",
                "description": "Analgesico",
                "dose": "5",
            }
        )
        medicine = Medi.objects.get(pk=1)

        self.assertEqual(medicine.dose, 5)

        # Intentamos actualizar la dosis con un valor inválido en este caso vacio
        medicine.update_medi({"dose": ""})

        # El valor de la dosis no debe haber cambiado
        medicine_updated = Medi.objects.get(pk=1)
        self.assertEqual(medicine_updated.dose, 5, "La dosis no debe cambiar si se proporciona un valor de dosis inválido")

class VetModelTest(TestCase):

    def test_can_create_and_get_vet(self):
        Vet.save_vet(
            {
                "name": "Mariano Navone",
                "phone": "2219870789",
                "email": "lanavoneta@gmail.com",
                "specialty": Vet.VetSpecialties.SIN_ESPECIALIDAD
            }
        )
        vets = Vet.objects.all()
        self.assertEqual(len(vets), 1)

        self.assertEqual(vets[0].name, "Mariano Navone")
        self.assertEqual(vets[0].phone, "2219870789")
        self.assertEqual(vets[0].email, "lanavoneta@gmail.com")
        self.assertEqual(vets[0].specialty, Vet.VetSpecialties.SIN_ESPECIALIDAD)

    def test_can_update_vet_specialty(self):
        Vet.save_vet(
            {
                "name": "Mariano Navone",
                "phone": "2219870789",
                "email": "lanavoneta@gmail.com",
                "specialty": Vet.VetSpecialties.SIN_ESPECIALIDAD
            }
        )
        vet = Vet.objects.get(pk=1)

        self.assertEqual(vet.specialty, Vet.VetSpecialties.SIN_ESPECIALIDAD)

        vet.update_vet({"specialty": Vet.VetSpecialties.CARDIOLOGIA})

        vet_updated = Vet.objects.get(pk=1)

        self.assertEqual(vet_updated.specialty, Vet.VetSpecialties.CARDIOLOGIA)

    def test_specialty_choices(self):
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

    def test_update_product_with_empty_price(self):
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

    def test_update_product_with_negative_price(self):
        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            }
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 100.0)

        product.update_product({"price": -100.0})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 100.0)

    def test_update_product_with_price_zero(self):
        Product.save_product(
            {
                "name": "Producto 1",
                "type": "Alimento",
                "price": 100.0,
            }
        )
        product = Product.objects.get(pk=1)

        self.assertEqual(product.price, 100.0)

        product.update_product({"price": 0.0})

        product_updated = Product.objects.get(pk=1)

        self.assertEqual(product_updated.price, 100.0)



class ProviderModelTest(TestCase):
    def test_can_create_and_get_provider(self):
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
