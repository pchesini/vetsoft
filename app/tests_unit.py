from django.test import TestCase
from app.models import Client, Medicine

class ClientModelTest(TestCase):
    def test_can_create_and_get_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
            }
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

    def test_can_update_client(self):
        Client.save_client(
            {
                "name": "Juan Sebastian Veron",
                "phone": "221555232",
                "address": "13 y 44",
                "email": "brujita75@hotmail.com",
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
                "email": "brujita75@hotmail.com",
            }
        )
        client = Client.objects.get(pk=1)

        self.assertEqual(client.phone, "221555232")

        client.update_client({"phone": ""})

        client_updated = Client.objects.get(pk=1)

        self.assertEqual(client_updated.phone, "221555232")

class MedicineModelTest(TestCase):
    def test_medicine_dose_range(self):
        # Crear una medicina con una dosis válida (5)
        valid_medicine_data = {
            "name": "Aspirina",
            "description": "Medicamento para el dolor de cabeza",
            "dose": "5"
        }
        errors = Medicine.validate_medicine(valid_medicine_data)
        self.assertEqual(len(errors), 0)

        # Crear una medicina con una dosis menor a 1
        low_dose_medicine_data = {
            "name": "Paracetamol",
            "description": "Medicamento para la fiebre",
            "dose": "0"
        }
        errors = Medicine.validate_medicine(low_dose_medicine_data)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "La dosis no puede ser negativa o valer 0")

        # Crear una medicina con una dosis mayor a 10
        high_dose_medicine_data = {
            "name": "Ibuprofeno",
            "description": "Medicamento para el dolor",
            "dose": "15"
        }
        errors = Medicine.validate_medicine(high_dose_medicine_data)
        self.assertIn("dose", errors)
        self.assertEqual(errors["dose"], "La dosis debe estar entre 1 y 10")
        
