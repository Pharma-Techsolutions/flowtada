# flowtada



#### 1. Install dependencies
```
# Create virtual environment
python3 -m venv flowtada-env

# Activate it
source flowtada-env/bin/activate
pip install -r requirements.txt
```
or 
```
# Create environment.yml
conda env create -f environment.yml

# Activate
conda activate flowtada
```

#### 1.a Generate a new secret key and Replace the generated key in .env
```
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
#### 2. Use Django commands to populate manage.py
```
django-admin startproject flowtada_temp .
```
#### 2.1 Create migrations
```
python manage.py makemigrations
```
#### 2.2 Apply migrations
```
python manage.py migrate
```

#### 2.3 Create superuser (admin)
```
python manage.py createsuperuser
```
#### 2.4 Collect static files
```
python manage.py collectstatic
```
#### 2..5 Run development server
```
python manage.py runserver
```