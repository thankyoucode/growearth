## 🌿 Online Plant Store Django Models Guide for Beginners

### 1. Project Setup
```bash
# Create Django Project
django-admin startproject plant_store
cd plant_store
python manage.py startapp plants
```

### 2. Model Definitions (models.py)
```python
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Plant(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    image = models.ImageField(upload_to='plant_images/')
    
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
```

### 3. Model Relationships 🔗

#### Key Connections:
- `Category` ➡️ `Plant`: One-to-Many
- `User` ➡️ `Order`: One-to-Many
- `Order` ➡️ `OrderItem`: One-to-Many
- `Plant` ➡️ `OrderItem`: One-to-Many

### 4. Database Migration Steps
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 5. Example Usage in Views
```python
def plant_list(request):
    # Get all available plants
    plants = Plant.objects.filter(stock__gt=0)
    return render(request, 'plant_list.html', {'plants': plants})

def create_order(request, plant_id):
    plant = Plant.objects.get(id=plant_id)
    order = Order.objects.create(
        user=request.user,
        total_price=plant.price
    )
    OrderItem.objects.create(
        order=order,
        plant=plant,
        quantity=1
    )
```

### 6. Best Practices 💡
- Always use `on_delete` in ForeignKey
- Add `__str__` method for readable representation
- Use type hints and validation
- Handle stock management carefully

### 7. Recommended Validations
```python
from django.core.validators import MinValueValidator

class Plant(models.Model):
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    stock = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
```

### 8. Admin Registration (admin.py)
```python
from django.contrib import admin
from .models import Plant, Category, Order

admin.site.register(Plant)
admin.site.register(Category)
admin.site.register(Order)
```

### 🚀 Quick Tips for Beginners
- Start simple
- Use Django's built-in User model
- Learn model relationships
- Practice creating and querying models
- Use Django shell for testing

### 📚 Learning Resources
- Django Official Documentation
- Django Girls Tutorial
- Real Python Django Tutorials
