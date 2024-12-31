# Project set up

## Set up new virtual environment
# ---- Windows ----- #
python -m venv env
.\env\Scripts\activate

# ----- MacOS/Linux ----- #
python -m venv env
source venv/bin/activate

# Pip install python packages
pip install --upgrade pip
pip install -r requirements.txt

# change directory to application
cd HowAreYou/

# Seed data using management command
python manage.py seed_db

# Run unit test
python manage.py test

# Django Admin credentials
username: admin
password: admin123

