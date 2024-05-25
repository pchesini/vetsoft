from django.test import TestCase
from app.models import Client, Medi

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
