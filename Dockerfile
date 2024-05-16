#Usamos como base la imagen oficial de python slim
FROM python:3.12-slim

#Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

#Copiamos los requerimientos al directorio de trabajo
COPY requirements.txt .

#Instalamos los paquetes requeridos dentro del contenedor
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos el resto de la aplicacion
COPY . .

#Exponemos el puerto para poder acceder desde afuera del contenedor
EXPOSE 8000

#Corremos el comando para iniciar la aplicacion
#CMD [ "python", "manage.py","runserver","0.0.0.0:8000" ]

# Copiamos el script de entrypoint y le damos permisos de ejecución
COPY entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

# Ejecutamos el script de entrypoint cuando se enciende el contenedor
ENTRYPOINT ["entrypoint.sh"]



