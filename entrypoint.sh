#!/bin/bash

# Esperamos a que las migraciones se completen.  
until python manage.py migrate 2>&1; do
  echo "La base de datos no está disponible todavía, esperando..."
  sleep 2
done

# Iniciamos la aplicación
exec python manage.py runserver 0.0.0.0:8000