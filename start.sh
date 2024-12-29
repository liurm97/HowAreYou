#!/bin/bash

# Project set up

## Set up virtual environment

### Windows
python -m venv env
.\env\Scripts\activate

### MacOS/Linux

# Pip install python packages
pip install --upgrade pip
pip install -r requirements.txt

# Create Django project
django-admin startproject HowAreYou

# Create application named `api`
python manage.py startapp api

# Create admin user
python manage.py createsuperuser


# Run test in verbose mode
python manage.py test -v 3


# Admin credentials
username: admin
password: admin123

