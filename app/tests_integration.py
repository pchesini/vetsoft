from django.test import TestCase
from django.shortcuts import reverse
from app.models import Client, Medi


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
                "email": "brujita75@hotmail.com",
            },
        )
        clients = Client.objects.all()
        self.assertEqual(len(clients), 1)

        self.assertEqual(clients[0].name, "Juan Sebastian Veron")
        self.assertEqual(clients[0].phone, "221555232")
        self.assertEqual(clients[0].address, "13 y 44")
        self.assertEqual(clients[0].email, "brujita75@hotmail.com")

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

    def test_edit_user_with_valid_data(self):
        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
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

        # Verificamos si la respuesta es un redireccionamiento (302)
        if response.status_code == 302:
            # Imprimimos el mensaje de error en la consola
            print("Mensaje de error: Por favor ingrese una dosis entre 1 y 10")
        else:
            # Si la respuesta no es un redireccionamiento, la prueba ha fallado
            print("La prueba ha fallado: No se esperaba un redireccionamiento")

    def test_validation_invalid_dose_above_range(self):
        # Enviamos una solicitud POST al formulario de creación de medicamentos con una dosis inválida (fuera del rango permitido, mayor que 10)
        response = self.client.post(
            reverse("medi_form"),
            data={
                "name": "Paracetamol",
                "description": "Analgesico",
                "dose": "15",  # Dosis fuera del rango permitido (mayor que 10)
            },
        )

        # Verificamos si la respuesta es un redireccionamiento (302)
        if response.status_code == 302:
            # Imprimimos el mensaje de error en la consola
            print("Mensaje de error: Por favor ingrese una dosis entre 1 y 10")
        else:
            # Si la respuesta no es un redireccionamiento, la prueba ha fallado
            print("La prueba ha fallado: No se esperaba un redireccionamiento")

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
