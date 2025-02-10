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

### Best Practices

- Separate apps into modular components
- Use nested template structure
- Organize static files by type
- Keep configuration in project root

Citations:
[1] https://forum.djangoproject.com/t/django-folder-file-structure/32287
[2] https://django-project-skeleton.readthedocs.io/en/latest/structure.html
