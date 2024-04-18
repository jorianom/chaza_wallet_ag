# Usar una imagen base de Python
FROM python:3

# Establecer el directorio de trabajo en /app
WORKDIR /app

# Copiar el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instalar las dependencias
RUN pip install -r requirements.txt

# Copiar el resto del código al contenedor
COPY . .

# Exponer el puerto 8000
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
