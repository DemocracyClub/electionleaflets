#! /bin/bash

python manage.py migrate
python manage.py uk_political_parties_load_parties
python manage.py constituencies_load_constituencies
