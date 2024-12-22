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

# Add api into project > settings.py

# Set up tests/ folder

# Run test in verbose mode
python manage.py test -v 3