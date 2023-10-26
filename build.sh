#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Realizar migraciones
python manage.py migrate

# Crear superusuario inicialmente
python manage.py shell < create_superuser.py

# Cargar datos desde archivos JSON
python manage.py loaddata fixtures/category_fixture.json
python manage.py loaddata fixtures/account_fixture.json
# Agrega comandos para cargar otros archivos JSON si es necesario