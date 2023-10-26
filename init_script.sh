#!/bin/bash

# Crear superusuario inicialmente
python manage.py shell < create_superuser.py

# Realizar migraciones
python manage.py migrate

# Cargar datos desde archivos JSON
python manage.py loaddata fixtures/category_fixture.json
python manage.py loaddata fixtures/account_fixture.json
python manage.py loaddata fixtures/inventory_fixture.json
# Agrega comandos para cargar otros archivos JSON si es necesario