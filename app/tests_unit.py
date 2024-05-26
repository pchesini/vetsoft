from django.test import TestCase
from app.models import Client,Vet



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
