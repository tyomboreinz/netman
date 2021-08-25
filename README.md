# Netman

IP Address Management and DHCP Server

## Requirement

Ubuntu / Debian

Package **isc-dhcp-server** and **nmap** already installed

Python 3.9.5

Django 3.2.4

## Installation

Migrate model to database

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Then insert default configuration of dhcp server

```bash
python3 manage.py loaddata data/*.json
```

insert user dan password

```bash
python3 manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'password')"
```

## Run Application

```bash
python3 manage.py runserver 0.0.0.0:8080
```

## Roadmap

- IP Address Management
- DHCP Server Management
- DNS Management
