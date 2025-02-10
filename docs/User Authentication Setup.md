## 🔐 User Authentication in Django Plant Store

### 1. User Authentication Setup

#### A. User Model Options

```python
# Option 1: Use Default Django User
from django.contrib.auth.models import User

# Option 2: Custom User Model (Recommended)
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
```

### 2. Authentication Views

```python
# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            # Return error message
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return redirect('home')
```

### 3. User Profile Model

```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    preferred_plants = models.ManyToManyField('Plant', blank=True)

    def __str__(self):
        return self.user.username
```

### 4. Authentication URLs

```python
# urls.py
from django.urls import path
from .views import login_user, register_user, logout_user

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('logout/', logout_user, name='logout'),
]
```

### 5. Login Required Decorator

```python
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def create_order(request):
    # Only logged-in users can create orders
    pass
```

### 6. HTML Templates

#### Login Template

```html
<!-- login.html -->
<form method="post">
  {% csrf_token %}
  <input type="text" name="username" placeholder="Username" />
  <input type="password" name="password" placeholder="Password" />
  <button type="submit">Login</button>
</form>
```

#### Registration Template

```html
<!-- register.html -->
<form method="post">
  {% csrf_token %} {{ form.as_p }}
  <button type="submit">Register</button>
</form>
```

### 7. Advanced Authentication Features

#### Password Reset

```python
# urls.py
from django.contrib.auth import views as auth_views

urlpatterns += [
    path('password_reset/',
         auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    # Other password reset URLs
]
```

### 8. Security Best Practices

- Use strong password validation
- Enable HTTPS
- Implement two-factor authentication
- Use Django's built-in protection against:
  - Cross-Site Request Forgery (CSRF)
  - Session hijacking
  - Password management

### 9. Permissions in Plant Store

```python
# Restrict order creation to authenticated users
@login_required
def create_order(request, plant_id):
    # Order creation logic

# Admin-only view
@user_passes_test(lambda u: u.is_staff)
def manage_inventory(request):
    # Inventory management
```

### 🚀 Quick Implementation Steps

1. Configure `INSTALLED_APPS` in `settings.py`
2. Run migrations
3. Create templates
4. Add URL configurations
5. Implement views

### 📚 Recommended Learning

- Django Authentication Documentation
- Real Python Authentication Tutorials
- Django Security Best Practices
