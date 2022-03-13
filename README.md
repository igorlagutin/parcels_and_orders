# igorlagutin Parcels and Orders
This service allows accounting incoming/out-coming parcels and internal orders and internal expenses for big b2b company

## Inbox parcels
This app allows performing accounting of parcels by their serial number

- The parcels can have different type and delivery company, quantity of places and notes;
- Search/filtering and print of undebt parcels is available;
- If parcel is older than 5 days and not debited it highlight in red colour;
- Now parcels of two Ukrainian delivery companies (Nova Poshta and Autolux) can send auto status and delivery destination API;
- Delivery status is automatically pull from delivers system on create and updates every 5 min until parcel marked as debited;
- All parcels status changes and status changes are logged;
- Track recently debited parcels.

## Steps to install

clone repo

[https://github.com/igorlagutin/parcels_and_orders.git](https://github.com/igorlagutin/parcels_and_orders.git)



### Setup environment

go to the project folder and run 
```
python3 -m venv env/parcels_and_orders
```
and then run

```
source env/parcels_and_orders/bin/activate
```

### Install requirements.txt
in project folder run
```
pip install -r requirements.txt
```

### external requirements
1) project use MySql database, you need install mysql-server and create database.
2) if you want to run periodic update of task status you need to install message broker RabbitMQ.
3) place env.py file in parcels_and_orders/parcels_and_orders, file should contain settings:

```
parcels_and_orders/parcels_and_orders/env.py

SECRET_KEY = 'django-strong-security-key'
DEBUG = False
ALLOWED_HOSTS = ["*"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "parcels_and_orders",
        "USER":"parcels_and_orders",
        "PASSWORD":"your_strong_pass",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            },
        'CHARSET': 'utf8',
        'COLLATION': 'utf8_general_ci',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
            }
    }
}
DRIVERS_PHONE = "" # phone of your regular parcel receiver at Nova Post
AUTOLUX_API_URL = "https://api.autolux-post.com.ua/"
AUTOLUX_API_LOGIN_URL = "https://api.autolux-post.com.ua/authentication/login/"
AUTOLUX_API_LOGIN = "" #your autolux login
AUTOLUX_API_PASS = "" #your autolux pass
NOVA_POST_API_URL = "https://api.novaposhta.ua/v2.0/json/"
```


### run application
```
./manage.py runserver
```

## Author
* **Igor Lagutin** 
Contact me at Linkedin  [https://www.linkedin.com/in/igorlagutin/](https://www.linkedin.com/in/igorlagutin/)
