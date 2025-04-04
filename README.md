## Django Project Structure for Grow Earth

### Project Root Structure

```
grow_earth/
│
├── project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   ├── plants/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   └── urls.py
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│       └── logo.png
│
├── templates/
│   ├── base.html
│   ├── components/
│   │   ├── header.html
│   │   └── footer.html
│   └── pages/
│       ├── home.html
│       └── plants.html
│
├── media/
├── requirements.txt
└── manage.py
```

### Key Directories Explained

- **`project/`**: Core Django project configuration
- **`apps/`**: Custom Django applications
- **`static/`**: Project-wide static files
- **`templates/`**: HTML templates
- **`media/`**: User-uploaded content
- **`manage.py`**: Django management script

