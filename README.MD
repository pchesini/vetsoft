# Vetsoft

Aplicación web para veterinarias utilizada en la cursada 2024 de Ingeniería y Calidad de Software. UTN-FRLP

## Integrantes

- Chesini Pablo
- Da Silva Franco
- Lucich Francisco
- Scianca Manuel

## Dependencias

- python 3
- Django
- sqlite
- playwright
- ruff

## Instalar dependencias

`pip install -r requirements.txt`

## Iniciar la Base de Datos

`python manage.py migrate`

## Iniciar app

`python manage.py runserver`

## Construir imagen docker

`docker build -t vetsoft-app:1.0 .`

## Desplegar contenedor

`docker run -d -p 8000:8000 --name "Vetsoft" vetsoft-app:1.0`

Luego se puede acceder a la aplicacion desde localhost:8000
