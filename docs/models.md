# Models.py in project (database table)

```python
import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)

    # Optional: Add profile-related fields
    profile_picture = models.ImageField(
        upload_to="profile_pics/", null=True, blank=True
    )

    bio = models.TextField(max_length=500, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def get_username(self):
        return self.username

    def full_name(self):  # Add method for full name
        return f"{self.first_name} {self.last_name}"

    def get_profile_picture(self):
        return self.profile_picture.url if self.profile_picture else None


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="category_images/")
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="subcategories",
        on_delete=models.SET_NULL,
    )
    is_featured = models.BooleanField(default=False)


class Product(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    description = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Enhanced Product Details
    scientific_name = models.CharField(max_length=100, null=True, blank=True)
    care_difficulty = models.CharField(
        max_length=20,
        choices=[
            ("EASY", "Easy"),
            ("MODERATE", "Moderate"),
            ("DIFFICULT", "Difficult"),
        ],
    )

    # Plant-Specific Attributes
    sunlight_requirements = models.CharField(
        max_length=50,
        choices=[
            ("FULL_SUN", "Full Sun"),
            ("PARTIAL_SUN", "Partial Sun"),
            ("SHADE", "Shade"),
        ],
    )
    water_frequency = models.CharField(
        max_length=50,
        choices=[("LOW", "Low"), ("MODERATE", "Moderate"), ("HIGH", "High")],
    )

    weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # For shipping

    images = models.ManyToManyField("ProductImage", related_name="product_images")
    inventory = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def discount_percentage(self):
        if self.sale_price:
            return ((self.price - self.sale_price) / self.price) * 100
        return 0


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)


class ProductImage(models.Model):
    image = models.ImageField(upload_to="product_images/")
    alt_text = models.CharField(max_length=100, null=True, blank=True)
    is_primary = models.BooleanField(default=False)


class CartItem(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ["user", "product"]


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("PROCESSING", "Processing"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    ]

    PAYMENT_METHODS = [
        ("COD", "Cash on Delivery"),
        ("CREDIT_CARD", "Credit Card"),
        ("DEBIT_CARD", "Debit Card"),
        ("UPI", "UPI"),
        ("NET_BANKING", "Net Banking"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="orders"
    )
    order_number = models.CharField(max_length=20, unique=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ("PENDING", "Pending"),
            ("COMPLETED", "Completed"),
            ("FAILED", "Failed"),
        ],
        default="PENDING",
    )

    shipping_address = models.TextField()
    billing_address = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number
            self.order_number = (
                f"GE-{timezone.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
            )
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price


class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="reviews", on_delete=models.CASCADE
    )
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["user", "product"]

```

## Comprehensive Model Analysis for Grow Earth Project

### 1. CustomUserManager

**Purpose**: Custom user creation and management
**Key Features**:

- Email normalization
- Flexible user creation
- Superuser creation with additional permissions

**Importance**:

- Provides custom authentication logic
- Enables email-based authentication
- Supports flexible user creation process

**Use Cases**:

- User registration
- Superuser creation
- Custom authentication workflows

### 2. CustomUser Model

**Purpose**: Comprehensive user representation
**Key Attributes**:

- UUID-based primary key
- Email as primary identifier
- Extended user profile information

**Advanced Features**:

- Verification status
- Profile picture
- Additional contact information
- Permissions management

**Long-Term Benefits**:

- Scalable user management
- Flexible authentication
- Enhanced user profile capabilities

### 3. Category Model

**Purpose**: Product categorization
**Key Features**:

- Hierarchical category structure
- Slug-based unique identification
- Featured category support

**Use Cases**:

- Organize plant collections
- Create nested category structures
- Highlight special categories

### 4. Product Model

**Purpose**: Detailed plant product representation
**Unique Characteristics**:

- Comprehensive plant-specific attributes
- Multiple image support
- Pricing flexibility
- Care difficulty classification

**Advanced Features**:

- Sunlight and water requirements
- Scientific name
- Inventory tracking
- Discount calculation

**Business Logic**:

- Dynamic pricing
- Detailed plant information
- Inventory management

### 5. CartItem Model

**Purpose**: Shopping cart management
**Key Features**:

- User-specific cart items
- Quantity tracking
- Price calculation

**Relationship Dynamics**:

- Connects User → Products
- Prevents duplicate cart entries

### 6. Order and OrderItem Models

**Purpose**: Order processing and tracking
**Comprehensive Features**:

- Multiple payment methods
- Detailed order status tracking
- Unique order number generation
- Payment status management

**Advanced Capabilities**:

- Flexible order workflow
- Comprehensive transaction tracking
- Supports multiple payment scenarios

### 7. Review and Wishlist Models

**Purpose**: User interaction and engagement
**Key Features**:

- Product rating system
- User-specific wishlists
- Review management

**Business Value**:

- Customer feedback collection
- Personalized user experience
- Product recommendation potential

## Architectural Strengths

### 1. Flexibility

- Modular design
- Easy to extend and customize
- Supports complex business logic

### 2. Scalability

- UUID-based primary keys
- Normalized database structure
- Efficient relationship management

### 3. Performance Considerations

- Indexed fields
- Efficient querying strategies
- Minimal database overhead

## Recommended Enhancements

1. Implement caching mechanisms
2. Add comprehensive validation
3. Create custom model methods
4. Develop robust serialization
5. Implement advanced search capabilities

## Best Practices Implemented

- Custom user authentication
- Comprehensive model relationships
- Detailed attribute tracking
- Flexible data management
- Scalable architecture

## Potential Future Integrations

- Machine learning recommendations
- Advanced analytics
- Third-party payment gateways
- Inventory management systems

## Learning Objectives

- Django ORM mastery
- Complex model relationship understanding
- Authentication system design
- E-commerce platform development

## Recommended Learning Path

1. Django documentation
2. ORM deep dive
3. Authentication system design
4. E-commerce platform architecture

This model structure provides a robust, flexible foundation for the Grow Earth project, balancing comprehensive functionality with clean, maintainable code.

Citations:

[1] https://learndjango.com/tutorials/django-custom-user-model
[2] https://www.javatpoint.com/django-custom-user-model
[3] https://dev.to/earthcomfy/getting-started-custom-user-model-5hc
[4] https://www.almabetter.com/bytes/tutorials/django/django-custom-user-model
[5] https://testdriven.io/blog/django-custom-user-model/
[6] https://www.horilla.com/blogs/how-to-build-a-custom-user-model-in-django/
[7] https://docs.djangoproject.com/en/5.1/topics/auth/customizing/
[8] https://www.youtube.com/watch?v=mndLkCEiflg
