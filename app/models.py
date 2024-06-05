from django.db import models

def validate_client(data):
    """
    Validate client data.

    Args:
    - data (dict): Dictionary containing client data.

    Returns:
    - dict: Dictionary containing errors, if any.
    """
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
    """
    Validate medicine data.

    Args:
    - data (dict): Dictionary containing medicine data.

    Returns:
    - dict: Dictionary containing errors, if any.
    """
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
    """
    Validate product data.

    Args:
    - data (dict): Dictionary containing product data.

    Returns:
    - dict: Dictionary containing errors, if any.
    """
    errors = {}

    name = data.get("name", "")
    type = data.get("type", "")
    price = data.get("price", "")

    if name == "":
        errors["name"] = "Por favor ingrese un nombre"

    if type == "":
        errors["type"] = "Por favor ingrese un tipo"

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
    """
    Validate provider data.

    Args:
    - data (dict): Dictionary containing provider data.

    Returns:
    - dict: Dictionary containing errors, if any.
    """
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
    """
    Model representing a client.

    Attributes:
    - name (str): The name of the client.
    - phone (str): The phone number of the client.
    - email (str): The email address of the client.
    - address (str, optional): The address of the client.
    """
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    @classmethod
    def save_client(cls, client_data):
        """
        Save a new client.

        Args:
        - client_data (dict): Dictionary containing client data.

        Returns:
        - tuple: A tuple containing a boolean indicating success and any errors, if any.
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
        """
        Update an existing client.

        Args:
        - client_data (dict): Dictionary containing client data to update.

        Returns:
        - None
        """
        self.name = client_data.get("name", "") or self.name
        self.email = client_data.get("email", "") or self.email
        self.phone = client_data.get("phone", "") or self.phone
        self.address
