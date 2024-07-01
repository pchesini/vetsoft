import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


def validate_name(name):
    if not re.match(r'^[a-zA-Z\s]+$', name):
        raise ValidationError('El nombre solo puede contener letras y espacios.')


def validate_client(data):
    errors = {}

    name = data.get("name", "")
    phone = str(data.get("phone", ""))  # Convertir a cadena

    #phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"
    else:
        try:
            validate_name(name)
        except ValidationError as e:
            errors["name"] = str(e)

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"
    elif not phone.startswith("54"):
        errors["phone"]="El teléfono debe comenzar con 54"
    elif not phone.isdigit():  # Verifica si el teléfono contiene solo dígitos
        errors["phone"] = "El teléfono debe ser numérico"


    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"
    elif email.split("@")[0] == "":
         errors["email"] = "Por favor ingrese un email valido"
    elif not email.endswith("@vetsoft.com"):
        errors["email"] = "Por favor ingrese un email terminado en @vetsoft.com"

    return errors


def validate_vet(data):
    errors = {}

    name = data.get("name", "")
    phone = data.get("phone", "")
    email = data.get("email", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if phone == "":
        errors["phone"] = "Por favor ingrese un teléfono"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    return errors



def validate_medicine(data):
        errors = {}

        name = data.get("name", "")
        description = data.get("description", "")
        dose = data.get("dose", "")

        if name == "":
            errors["name"] = "Por favor ingrese un nombre"

        if description == "":
            errors["description"] = "Por favor ingrese una descripcion"

        if dose == "":
            errors["dose"] = "Por favor ingrese una dosis"
        else:
            try:
                dose_value = int(dose)
                if dose_value < 1 or dose_value > 10:
                    errors["dose"] = "Por favor ingrese una dosis entre 1 y 10"
            except ValueError:
             errors["dose"] = "La dosis debe ser un número entero"

        return errors

def validate_product(data):
    errors = {}

    name = data.get("name", "")
    type = data.get("type", "")
    price = data.get("price", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if type == "":
        errors["type"] = "Por favor ingrese un tipo"

    '''if price == "":
        errors["price"] = "Por favor ingrese un precio"
    elif float(price) <= 0:
        errors["price"] = "Por favor ingrese un precio mayor a cero"
    '''
    if price == "":
        errors["price"] = "Por favor ingrese un precio"
    else:
        try:
            price_float = float(price)
            if price_float <= 0:
                errors["price"] = "Por favor ingrese un precio mayor a cero"
        except ValueError:
            errors["price"] = "Por favor ingrese un precio válido"

    return errors


def validate_provider(data):
    errors = {}

    name = data.get("name", "")
    email = data.get("email", "")
    address = data.get("address", "")


    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if email == "":
        errors["email"] = "Por favor ingrese un email"
    elif email.count("@") == 0:
        errors["email"] = "Por favor ingrese un email valido"

    if address == "":
        errors["address"] = "Por favor ingrese una dirección"


    return errors


class Client(models.Model):
    """Representa un cliente con detalles de contacto personal.

    Attributes:
        name (str): El nombre del cliente.
        phone (str): El número de teléfono del cliente.
        email (str): La dirección de correo electrónico del cliente.
        address (str): La dirección física del cliente.
    """
    name = models.CharField(max_length=100)
    phone = models.BigIntegerField(
        validators=[
            RegexValidator(
                regex=r'^\d+$',
                message="El teléfono debe contener solo números.",
            ),
        ])
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        """
        Guarda un nuevo cliente en la base de datos.
        """
        errors = validate_client(client_data)

        if len(errors.keys()) > 0:
            return False, errors

        Client.objects.create(
            name=client_data.get("name"),
            phone=client_data.get("phone"),
            email=client_data.get("email"),
            address=client_data.get("address"),
        )

        return True, None

    def update_client(self, client_data):
        """Actualizar datos de un cliente"""
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address = client_data.get("address", "") or self.address

         # Validar los datos actualizados
        updated_data = {
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
        }
        errors = validate_client(updated_data)
        if errors:
            return False, errors

        self.save()
        return True, None

class Product(models.Model):
    """Representa un producto disponible para la venta.

    Attributes:
        name (str): El nombre del producto.
        type (str): El tipo o categoría del producto.
        price (float): El precio del producto.
    """
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    price = models.FloatField()

    def __str__(self):
        return self.name

    @classmethod
    def save_product(cls, product_data):
        """Guarda un nuevo producto en la base de datos"""
        errors = validate_product(product_data)

        if len(errors.keys()) > 0:
            return False, errors

        Product.objects.create(
            name=product_data.get("name"),
            type=product_data.get("type"),
            price=product_data.get("price"),
        )

        return True, None

    def update_product(self, product_data):
        """Actualiza los datos de un producto"""
        self.name = product_data.get("name", "") or self.name
        self.type = product_data.get("type", "") or self.type
        try:
            price = float(product_data.get("price", ""))
        except ValueError:
        # Si el precio no es un valor numérico válido, retorna un mensaje de error
            return False, {"price": "Por favor ingrese un precio válido"}

        if price <= 0:
        # Si el precio es menor o igual a cero, retorna un mensaje de error
            return False, {"price": "Por favor ingrese un precio mayor a cero"}

        # Si no hay errores, actualiza el precio y guarda el objeto en la base de datos
        self.price = price
        self.save()
        return True, None

class Vet(models.Model):
    """Representa un veterinario con una especialidad específica.

    Attributes:
        name (str): El nombre del veterinario.
        email (str): La dirección de correo electrónico del veterinario.
        phone (str): El número de teléfono del veterinario.
        specialty (str): La especialidad del veterinario.
    """
    class VetSpecialties(models.TextChoices):
        SIN_ESPECIALIDAD="Sin especialidad", _("Sin especialidad")
        CARDIOLOGIA="Cardiología", _("Cardiología")
        MEDICINA_INTERNA_PEQUENOS_ANIMALES="Medicina interna de pequeños animales", _("Medicina interna de pequeños animales")
        MEDICINA_INTERNA_GRANDES_ANIMALES="Medicina interna de grandes animales", _("Medicina interna de grandes animales")
        NEUROLOGIA="Neurología", _("Neurología")
        ONCOLOGIA="Oncología", _("Oncología")
        NUTRICION="Nutrición", _("Nutrición")


    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    specialty = models.CharField(
        max_length=100,
        choices=VetSpecialties,
        default=VetSpecialties.SIN_ESPECIALIDAD, # se agrego la coma faltante detectada con ruff
    )

    def __str__(self):
        return self.name

    @classmethod
    def save_vet(cls, vet_data):
        """"Guarda un nuevo veterinario en la base de datos"""
        errors = validate_vet(vet_data)

        if len(errors.keys()) > 0:
            return False, errors

        Vet.objects.create(
            name=vet_data.get("name"),
            phone=vet_data.get("phone"),
            email=vet_data.get("email"),
            specialty=vet_data.get("specialty"),
        )

        return True, None

    def update_vet(self, vet_data):
        """Actualiza los datos de un veterinario"""
        self.name = vet_data.get("name", "") or self.name
        self.email = vet_data.get("email", "") or self.email
        self.phone = vet_data.get("phone", "") or self.phone
        self.specialty = vet_data.get("specialty", "") or self.specialty
        self.save()


class Medi(models.Model):
    """Representa una medicina.

    Attributes:
        name (str): El nombre de la medicina.
        description (str): La descripción de la medicina.
        dose (int): La dosis de la medicina.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()
    dose = models.IntegerField()

    def __str__(self):
        return self.name

    @classmethod
    def save_medi(cls, medi_data):
        """"Guarda un nuevo medicamento en la base de datos"""
        errors = validate_medicine(medi_data)

        if len(errors.keys()) > 0:
            return False, errors

        Medi.objects.create(
            name=medi_data.get("name"),
            description=medi_data.get("description"),
            dose=medi_data.get("dose"),
        )

        return True, None

    def update_medi(self, medi_data):
        """Actualiza los datos de un medicamento"""
        self.name = medi_data.get("name", "") or self.name
        self.description = medi_data.get("description", "") or self.description
        self.dose = medi_data.get("dose", "") or self.dose
        self.save()


class Provider(models.Model):
    """Representa un proveedor.

     Attributes:
         name (str): El nombre del proveedor.
         email (str): La dirección de correo electrónico del proveedor.
         address (str, opcional): La dirección física del proveedor.
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_provider(cls, provider_data):
        """"Guarda un nuevo proveedor en la base de datos"""
        errors = validate_provider(provider_data)

        if len(errors.keys()) > 0:
            return False, errors

        Provider.objects.create(
            name=provider_data.get("name"),
            email=provider_data.get("email"),
            address=provider_data.get("address"),

        )

        return True, None

    def update_provider(self, provider_data):
        """"Actualiza los datos de un proveedor"""
        self.name = provider_data.get("name","") or self.name
        self.email = provider_data.get("email","") or self.email
        self.address = provider_data.get("address","") or self.address

        self.save()
