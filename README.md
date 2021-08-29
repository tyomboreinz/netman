# Netman

IP Address, DHCP Server, DNS, Portal App Management for Your Intranet

## Requirement

Ubuntu / Debian

Package **nmap**, **isc-dhcp-server**, **bind9** already installed

Python 3.9.5

## Installation

Install some requirement for Python using pip

```bash
pip install -r requirement.txt
```

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
- Portal APP Management