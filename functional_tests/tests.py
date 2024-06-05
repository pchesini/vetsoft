import os

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from playwright.sync_api import Browser, expect, sync_playwright

from app.models import Client, Medi, Product, Provider, Vet

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
playwright = sync_playwright().start()
headless = os.environ.get("HEADLESS", 1) == 1
#headless = os.environ.get("HEADLESS", "0") == 1
slow_mo = os.environ.get("SLOW_MO", 0)

class PlaywrightTestCase(StaticLiveServerTestCase):
    """Clase base para pruebas de Playwright."""
    @classmethod
    def setUpClass(cls):
        "Configura el navegador"
        super().setUpClass()
        cls.browser: Browser = playwright.firefox.launch(
            headless=headless, slow_mo=int(slow_mo)
        )

    @classmethod
    def tearDownClass(cls):
        "Asegura que el navegador se cierre correctamente al finalizar todas las pruebas"
        super().tearDownClass()
        cls.browser.close()

    def setUp(self):
        "Garantiza que cada prueba comience con una nueva pagina en el navegador"
        super().setUp()
        self.page = self.browser.new_page()

    def tearDown(self):
        "Aseguro que cada prueba se limpie adecuadamente despues de ejecutarse"
        super().tearDown()
        self.page.close()


class HomeTestCase(PlaywrightTestCase):
    """Verifica que la página de inicio tenga una barra de navegación con enlaces."""
    def test_should_have_navbar_with_links(self):
        """Verifica que la página de inicio tenga tarjetas con enlaces."""

        self.page.goto(self.live_server_url)

        navbar_home_link = self.page.get_by_test_id("navbar-Home")

        expect(navbar_home_link).to_be_visible()
        expect(navbar_home_link).to_have_text("Home")
        expect(navbar_home_link).to_have_attribute("href", reverse("home"))

        navbar_clients_link = self.page.get_by_test_id("navbar-Clientes")

        expect(navbar_clients_link).to_be_visible()
        expect(navbar_clients_link).to_have_text("Clientes")
        expect(navbar_clients_link).to_have_attribute("href", reverse("clients_repo"))

    def test_should_have_home_cards_with_links(self):
        """Verifica que la página de inicio tenga tarjetas con enlaces."""

        self.page.goto(self.live_server_url)

        home_clients_link = self.page.get_by_test_id("home-Clientes")

        expect(home_clients_link).to_be_visible()
        expect(home_clients_link).to_have_text("Clientes")
        expect(home_clients_link).to_have_attribute("href", reverse("clients_repo"))

        self.page.goto(self.live_server_url)

        home_products_link = self.page.get_by_test_id("home-Productos")

        expect(home_products_link).to_be_visible()
        expect(home_products_link).to_have_text("Productos")
        expect(home_products_link).to_have_attribute("href", reverse("products_repo"))

class ClientsRepoTestCase(PlaywrightTestCase):
    """Pruebas para el repositorio de clientes."""

    def test_should_show_message_if_table_is_empty(self):
        """Verifica que se muestre un mensaje si la tabla está vacía."""

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).to_be_visible()

    def test_should_show_clients_data(self):
        """Verifica que se muestren los datos de los clientes."""

        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        Client.objects.create(
            name="Guido Carrillo",
            address="1 y 57",
            phone="221232555",
            email="goleador@gmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("No existen clientes")).not_to_be_visible()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

    def test_should_show_add_client_action(self):
        """Verifica que se muestre la acción para agregar un cliente."""

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        add_client_action = self.page.get_by_role(
            "link", name="Nuevo cliente", exact=False
        )
        expect(add_client_action).to_have_attribute("href", reverse("clients_form"))

    def test_should_show_client_edit_action(self):
        """Verifica que se muestre la acción para editar un cliente."""

        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )

    def test_should_show_client_delete_action(self):
        """Verifica que se muestre la acción para eliminar un cliente."""

        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de cliente"
        )
        client_id_input = edit_form.locator("input[name=client_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("clients_delete"))
        expect(client_id_input).not_to_be_visible()
        expect(client_id_input).to_have_value(str(client.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_client(self):
        """Verifica que se pueda eliminar un cliente."""

        Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        self.page.goto(f"{self.live_server_url}{reverse('clients_repo')}")

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("clients_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()


class ClientCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_client(self):
        """Verifica que se pueda eliminar un cliente."""

        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75@hotmail.com")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).to_be_visible()
        expect(self.page.get_by_text("221555232")).to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 44")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """Verifica que se muestren errores si el formulario es inválido."""

        self.page.goto(f"{self.live_server_url}{reverse('clients_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Juan Sebastián Veron")
        self.page.get_by_label("Teléfono").fill("221555232")
        self.page.get_by_label("Email").fill("brujita75")
        self.page.get_by_label("Dirección").fill("13 y 44")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_client(self):
        """Verifica que se pueda editar un cliente."""

        client = Client.objects.create(
            name="Juan Sebastián Veron",
            address="13 y 44",
            phone="221555232",
            email="brujita75@hotmail.com",
        )

        path = reverse("clients_edit", kwargs={"id": client.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Guido Carrillo")
        self.page.get_by_label("Teléfono").fill("221232555")
        self.page.get_by_label("Email").fill("goleador@gmail.com")
        self.page.get_by_label("Dirección").fill("1 y 57")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Juan Sebastián Veron")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 44")).not_to_be_visible()
        expect(self.page.get_by_text("221555232")).not_to_be_visible()
        expect(self.page.get_by_text("brujita75@hotmail.com")).not_to_be_visible()

        expect(self.page.get_by_text("Guido Carrillo")).to_be_visible()
        expect(self.page.get_by_text("1 y 57")).to_be_visible()
        expect(self.page.get_by_text("221232555")).to_be_visible()
        expect(self.page.get_by_text("goleador@gmail.com")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("clients_edit", kwargs={"id": client.id})
        )


class MedicineCreateEditTestCase(PlaywrightTestCase):
    def test_should_be_able_to_create_a_new_medicine(self):
        """Verifica que se pueda crear un nuevo medicamento."""
        self.page.goto(f"{self.live_server_url}{reverse('medi_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("ibuprofeno")
        self.page.get_by_label("Descripcion").fill("para el dolor")
        self.page.get_by_label("Dosis").fill("5")


        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("ibuprofeno")).to_be_visible()
        expect(self.page.get_by_text("para el dolor")).to_be_visible()
        expect(self.page.get_by_text("5")).to_be_visible()
        

    def test_should_view_errors_if_form_is_invalid(self):
        """Verifica que se muestren errores si el formulario es inválido."""

        self.page.goto(f"{self.live_server_url}{reverse('medi_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una descripcion")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dosis")).to_be_visible()

        self.page.get_by_label("Nombre").fill("ibuprofeno")
        self.page.get_by_label("Descripcion").fill("para el dolor")
        self.page.get_by_label("Dosis").fill("0")
        
      

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(
            self.page.get_by_text("Por favor ingrese una descripcion")
        ).not_to_be_visible()

    """  expect(
            self.page.get_by_text("Por favor ingrese una dosis entre 1 y 10")
        ).to_be_visible() 
        self.page.get_by_label("Dosis").fill("")
        expect(
            self.page.get_by_text("Por favor ingrese una dosis")
        ).to_be_visible() """
        
    def test_should_be_able_to_edit_a_medicine(self):
        """Verifica que se pueda editar un medicamento."""

        medi = Medi.objects.create(
            name="ibuprofeno",
            description="para el dolor",
            dose="5",
           
        )

        path = reverse("medi_edit", kwargs={"id": medi.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("paracetamol")
        self.page.get_by_label("Descripcion").fill("para la fiebre")
        self.page.get_by_label("Dosis").fill("8")
        

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("ibuprofeno")).not_to_be_visible()
        expect(self.page.get_by_text("para el dolor")).not_to_be_visible()
        expect(self.page.get_by_text("5")).not_to_be_visible()
     

        expect(self.page.get_by_text("paracetamol")).to_be_visible()
        expect(self.page.get_by_text("para la fiebre")).to_be_visible()
        expect(self.page.get_by_text("8")).to_be_visible()
        

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("medi_edit", kwargs={"id": medi.id})
        )

class ProductsRepoTestCase(PlaywrightTestCase):
    def test_should_show_message_if_table_is_empty(self):
        """Verifica que se muestre un mensaje si la tabla está vacía."""

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("No existen productos")).to_be_visible()

    def test_should_show_products_data(self):
        """Verifica que se muestren los datos de los productos."""

        Product.objects.create(
            name="Producto A",
            type="Tipo A",
            price=100.0,
        )

        Product.objects.create(
            name="Producto B",
            type="Tipo B",
            price=200.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("No existen productos")).not_to_be_visible()

        expect(self.page.get_by_text("Producto A")).to_be_visible()
        expect(self.page.get_by_text("Tipo A")).to_be_visible()
        expect(self.page.get_by_text("100.0")).to_be_visible()

        expect(self.page.get_by_text("Producto B")).to_be_visible()
        expect(self.page.get_by_text("Tipo B")).to_be_visible()
        expect(self.page.get_by_text("200.0")).to_be_visible()

    def test_should_show_add_product_action(self):
        """Verifica que se muestre la acción para agregar un producto."""

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        add_product_action = self.page.get_by_role(
            "link", name="Nuevo producto", exact=False
        )
        expect(add_product_action).to_have_attribute("href", reverse("products_form"))

    def test_should_show_product_edit_action(self):
        """Verifica que se muestre la acción para editar un producto."""

        product = Product.objects.create(
            name="Producto A",
            type="Tipo A",
            price=100.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("products_edit", kwargs={"id": product.id})
        )

    def test_should_show_product_delete_action(self):
        """Verifica que se muestre la acción para eliminar un producto."""

        product = Product.objects.create(
            name="Producto A",
            type="Tipo A",
            price=100.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de producto"
        )
        product_id_input = edit_form.locator("input[name=product_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("products_delete"))
        expect(product_id_input).not_to_be_visible()
        expect(product_id_input).to_have_value(str(product.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_product(self):
        """Verifica que se pueda eliminar un producto."""

        Product.objects.create(
            name="Producto A",
            type="Tipo A",
            price=100.0,
        )

        self.page.goto(f"{self.live_server_url}{reverse('products_repo')}")

        expect(self.page.get_by_text("Producto A")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("products_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Producto A")).not_to_be_visible()


class ProductCreateEditTestCase(PlaywrightTestCase):

    def test_should_be_able_to_create_a_new_product(self):
        """Verifica que se pueda crear un nuevo producto."""

        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Producto A")
        self.page.get_by_label("Tipo").fill("Tipo A")
        self.page.get_by_label("Precio").fill("100.0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Producto A")).to_be_visible()
        expect(self.page.get_by_text("Tipo A")).to_be_visible()
        expect(self.page.get_by_text("100.0")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """Verifica que se muestren errores si el formulario es inválido."""

        self.page.goto(f"{self.live_server_url}{reverse('products_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un tipo")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un precio")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Producto A")
        self.page.get_by_label("Tipo").fill("Tipo A")
        self.page.get_by_label("Precio").fill("-100.0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un tipo")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un precio mayor a cero")).to_be_visible()

        self.page.get_by_label("Precio").fill("0.0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un tipo")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un precio mayor a cero")).to_be_visible()

    def test_should_be_able_to_edit_a_product(self):
        """Verifica que se pueda editar un producto existente."""

        product = Product.objects.create(
            name="Producto A",
            type="Tipo A",
            price=100.0,
        )

        path = reverse("products_edit", kwargs={"id": product.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Producto B")
        self.page.get_by_label("Tipo").fill("Tipo B")
        self.page.get_by_label("Precio").fill("200.0")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Producto A")).not_to_be_visible()
        expect(self.page.get_by_text("Tipo A")).not_to_be_visible()
        expect(self.page.get_by_text("100.0")).not_to_be_visible()

        expect(self.page.get_by_text("Producto B")).to_be_visible()
        expect(self.page.get_by_text("Tipo B")).to_be_visible()
        expect(self.page.get_by_text("200.0")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("products_edit", kwargs={"id": product.id})
        )


class VetRepoTestCase(PlaywrightTestCase):
    """Casos de prueba para el repositorio de veterinarios."""

    def test_should_show_message_if_table_is_empty(self):
        """Debe mostrar un mensaje si la tabla está vacía."""

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("No existen veterinarios")).to_be_visible()

    def test_should_show_vets_data(self):
        """Debe mostrar los datos de los veterinarios."""

        Vet.objects.create(
            name = "Mariano Navone",
            phone = "2219870789",
            email = "lanavoneta@gmail.com",
            specialty = Vet.VetSpecialties.SIN_ESPECIALIDAD
        )

        Vet.objects.create(
            name="Tomás Martín Etcheverry",
            phone="2217462854",
            email="tetcheverry@gmail.com",
            specialty = Vet.VetSpecialties.CARDIOLOGIA
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("No existen veterinarios")).not_to_be_visible()

        expect(self.page.get_by_text("Mariano Navone")).to_be_visible()
        expect(self.page.get_by_text("2219870789")).to_be_visible()
        expect(self.page.get_by_text("lanavoneta@gmail.com")).to_be_visible()
        expect(self.page.get_by_text(Vet.VetSpecialties.SIN_ESPECIALIDAD)).to_be_visible()

        expect(self.page.get_by_text("Tomás Martín Etcheverry")).to_be_visible()
        expect(self.page.get_by_text("2217462854")).to_be_visible()
        expect(self.page.get_by_text("tetcheverry@gmail.com")).to_be_visible()
        expect(self.page.get_by_text(Vet.VetSpecialties.CARDIOLOGIA)).to_be_visible()

    def test_should_show_add_vet_action(self):
        """Debe mostrar la acción para agregar un veterinario."""

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        add_vet_action = self.page.get_by_role(
            "link", name="Nuevo Veterinario", exact=False
        )
        expect(add_vet_action).to_have_attribute("href", reverse("vets_form"))

    def test_should_show_vet_edit_action(self):
        """Debe mostrar la acción para editar un veterinario."""

        vet = Vet.objects.create(
            name = "Mariano Navone",
            phone = "2219870789",
            email = "lanavoneta@gmail.com",
            specialty = Vet.VetSpecialties.SIN_ESPECIALIDAD
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("vets_edit", kwargs={"id": vet.id})
        )

    def test_should_show_vet_delete_action(self):
        """Debe mostrar la acción para eliminar un veterinario."""

        vet = Vet.objects.create(
            name = "Mariano Navone",
            phone = "2219870789",
            email = "lanavoneta@gmail.com",
            specialty = Vet.VetSpecialties.SIN_ESPECIALIDAD
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        edit_form = self.page.get_by_role(
            "form", name="Formulario de eliminación de veterinario"
        )
        vet_id_input = edit_form.locator("input[name=vet_id]")

        expect(edit_form).to_be_visible()
        expect(edit_form).to_have_attribute("action", reverse("vets_delete"))
        expect(vet_id_input).not_to_be_visible()
        expect(vet_id_input).to_have_value(str(vet.id))
        expect(edit_form.get_by_role("button", name="Eliminar")).to_be_visible()

    def test_should_can_be_able_to_delete_a_vet(self):
        """Debe poder eliminar un veterinario."""

        Vet.objects.create(
            name = "Mariano Navone",
            phone = "2219870789",
            email = "lanavoneta@gmail.com",
            specialty = Vet.VetSpecialties.SIN_ESPECIALIDAD
        )

        self.page.goto(f"{self.live_server_url}{reverse('vets_repo')}")

        expect(self.page.get_by_text("Mariano Navone")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("vets_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Mariano Navone")).not_to_be_visible()

class VetCreateEditTestCase(PlaywrightTestCase):
    
    def test_should_be_able_to_create_a_new_vet(self):
        """
        Prueba que un nuevo veterinario pueda ser creado.
        """
        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Mariano Navone")
        self.page.get_by_label("Teléfono").fill("2219870789")
        self.page.get_by_label("Email").fill("lanavoneta@gmail.com")
        self.page.get_by_label("Especialidad").select_option("Cardiología")





        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Mariano Navone")).to_be_visible()
        expect(self.page.get_by_text("2219870789")).to_be_visible()
        expect(self.page.get_by_text("lanavoneta@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("Cardiología")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """
        Prueba que se muestren errores si el formulario es inválido.
        """
        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un teléfono")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Mariano Navone")
        self.page.get_by_label("Teléfono").fill("2219870789")
        self.page.get_by_label("Email").fill("lanavonetagmail.com")
        self.page.get_by_label("Especialidad").select_option("Cardiología")

        self.page.get_by_role("button", name="Guardar").click()

        expect(
            self.page.get_by_text("Por favor ingrese un nombre")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un teléfono")
        ).not_to_be_visible()

        expect(
            self.page.get_by_text("Por favor ingrese un email valido")
        ).to_be_visible()

    def test_should_be_able_to_edit_a_vet(self):
        """
        Prueba que se pueda editar un veterinario.
        """
        vet = Vet.objects.create(
            name = "Mariano Navone",
            phone = "2219870789",
            email = "lanavoneta@gmail.com",
            specialty = Vet.VetSpecialties.SIN_ESPECIALIDAD
        )

        path = reverse("vets_edit", kwargs={"id": vet.id})
        self.page.goto(f"{self.live_server_url}{path}")


        self.page.get_by_label("Nombre").fill("Tomás Martín Etcheverry")
        self.page.get_by_label("Teléfono").fill("2217462854")
        self.page.get_by_label("Email").fill("tetcheverry@gmail.com")
        self.page.get_by_label("Especialidad").select_option("Cardiología")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Mariano Navone")).not_to_be_visible()
        expect(self.page.get_by_text("2219870789")).not_to_be_visible()
        expect(self.page.get_by_text("lanavoneta@gmail.com")).not_to_be_visible()
        expect(self.page.get_by_text("Sin especialidad")).not_to_be_visible()

        expect(self.page.get_by_text("Tomás Martín Etcheverry")).to_be_visible()
        expect(self.page.get_by_text("2217462854")).to_be_visible()
        expect(self.page.get_by_text("tetcheverry@gmail.com")).to_be_visible()
        expect(self.page.get_by_text("Cardiología")).to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("vets_edit", kwargs={"id": vet.id})
        )

    def test_can_select_every_specialty_on_create(self):
        """
        Prueba que se puedan seleccionar todas las especialidades al crear un veterinario.
        """
        self.page.goto(f"{self.live_server_url}{reverse('vets_form')}")

        for option in Vet.VetSpecialties:
            self.page.get_by_label("Especialidad").select_option(option)
            expect(self.page.get_by_label("Especialidad")).to_have_value(option)

    def test_can_select_every_specialty_on_edit(self):
        """
        Prueba que se puedan seleccionar todas las especialidades al editar un veterinario.
        """

        vet = Vet.objects.create(
            name = "Mariano Navone",
            phone = "2219870789",
            email = "lanavoneta@gmail.com",
            specialty = Vet.VetSpecialties.SIN_ESPECIALIDAD
        )

        path = reverse("vets_edit", kwargs={"id": vet.id})
        self.page.goto(f"{self.live_server_url}{path}")

        for option in Vet.VetSpecialties:
            self.page.get_by_label("Especialidad").select_option(option)
            expect(self.page.get_by_label("Especialidad")).to_have_value(option)

class ProviderRepoTestCase(PlaywrightTestCase):
    """
    Caso de prueba para el repositorio de proveedores.
    """
    def test_should_show_message_if_table_is_empty(self):
        """
        Prueba que se muestre un mensaje si la tabla está vacía.
        """
        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).to_be_visible()

    def test_should_show_providers_data(self):
        """
        Prueba que se muestren los datos de los proveedores correctamente.
        """
        Provider.objects.create(
            name="Proveedor Ejemplo",
            email="proveedor@ejemplo.com",
            address="13 y 32",
        )

        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        expect(self.page.get_by_text("No existen proveedores")).not_to_be_visible()

        expect(self.page.get_by_text("Proveedor Ejemplo")).to_be_visible()
        expect(self.page.get_by_text("proveedor@ejemplo.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 32")).to_be_visible()

    def test_should_show_add_provider_action(self):
        """
        Prueba que se muestre la acción 'Agregar proveedor'.
        """
        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        add_provider_action = self.page.get_by_role(
            "link", name="Nuevo proveedor", exact=False
        )
        expect(add_provider_action).to_have_attribute("href", reverse("provider_form"))

    def test_should_show_provider_edit_action(self):
        """
        Prueba que se muestre la acción 'Editar proveedor'.
        """
        provider = Provider.objects.create(
            name="Proveedor Ejemplo",
            email="proveedor@ejemplo.com",
            address="13 y 32",
        )

        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("provider_edit", kwargs={"id": provider.id})
        )

    def test_should_can_be_able_to_delete_a_provider(self):
        """
        Prueba que se pueda eliminar un proveedor.
        """
        Provider.objects.create(
            name="Proveedor Ejemplo",
            email="proveedor@ejemplo.com",
            address="13 y 32",
        )

        self.page.goto(f"{self.live_server_url}{reverse('provider_repo')}")

        expect(self.page.get_by_text("Proveedor Ejemplo")).to_be_visible()

        def is_delete_response(response):
            return response.url.find(reverse("provider_delete"))

        # verificamos que el envio del formulario fue exitoso
        with self.page.expect_response(is_delete_response) as response_info:
            self.page.get_by_role("button", name="Eliminar").click()

        response = response_info.value
        self.assertTrue(response.status < 400)

        expect(self.page.get_by_text("Proveedor Ejemplo")).not_to_be_visible()


class ProviderCreateEditTestCase(PlaywrightTestCase):
    """
    Caso de prueba para crear y editar proveedores.
    """
    def test_should_be_able_to_create_a_new_provider(self):
        """
        Prueba que se pueda crear un nuevo proveedor.
        """
        self.page.goto(f"{self.live_server_url}{reverse('provider_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Proveedor Ejemplo")
        self.page.get_by_label("Email").fill("proveedor@ejemplo.com")
        self.page.get_by_label("Dirección").fill("13 y 32")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Proveedor Ejemplo")).to_be_visible()
        expect(self.page.get_by_text("proveedor@ejemplo.com")).to_be_visible()
        expect(self.page.get_by_text("13 y 32")).to_be_visible()

    def test_should_view_errors_if_form_is_invalid(self):
        """
        Prueba que se muestren errores si el formulario es inválido.
        """
        self.page.goto(f"{self.live_server_url}{reverse('provider_form')}")

        expect(self.page.get_by_role("form")).to_be_visible()

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dirección")).to_be_visible()

        self.page.get_by_label("Nombre").fill("Proveedor Ejemplo")
        self.page.get_by_label("Email").fill("proveedor@ejemplo.com")
        self.page.get_by_label("Dirección").fill("13 y 32")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_text("Por favor ingrese un nombre")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese un email")).not_to_be_visible()
        expect(self.page.get_by_text("Por favor ingrese una dirección")).not_to_be_visible()

    def test_should_be_able_to_edit_a_provider(self):
        """
        Prueba que se pueda editar un proveedor.
        """
        provider = Provider.objects.create(
            name="Proveedor Ejemplo",
            email="proveedor@ejemplo.com",
            address="13 y 32",
        )

        path = reverse("provider_edit", kwargs={"id": provider.id})
        self.page.goto(f"{self.live_server_url}{path}")

        self.page.get_by_label("Nombre").fill("Nuevo Proveedor")
        self.page.get_by_label("Email").fill("nuevo@proveedor.com")
        self.page.get_by_label("Dirección").fill("Nueva Calle 123")

        self.page.get_by_role("button", name="Guardar").click()

        expect(self.page.get_by_role("link", name="Nuevo Proveedor")).to_be_visible()
        expect(self.page.get_by_text("nuevo@proveedor.com")).to_be_visible()
        expect(self.page.get_by_text("Nueva Calle 123")).to_be_visible()

        expect(self.page.get_by_text("Proveedor Ejemplo")).not_to_be_visible()
        expect(self.page.get_by_text("proveedor@ejemplo.com")).not_to_be_visible()
        expect(self.page.get_by_text("13 y 32")).not_to_be_visible()

        edit_action = self.page.get_by_role("link", name="Editar")
        expect(edit_action).to_have_attribute(
            "href", reverse("provider_edit", kwargs={"id": provider.id})
        )
