import uuid

from django.db import models
from django.utils import timezone

from ..account.models import CustomUser


class Tag(models.Model):
    tag = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)


class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="category_images/", null=True, blank=True)
    slug = models.SlugField(unique=True)
    # is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Plant(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="plants"
    )
    image = models.ImageField(upload_to="plant_images/", null=True, blank=True)
    description = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )

    # Enhanced Plant Details
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

    inventory = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def discount_percentage(self):
        if self.sale_price:
            return ((self.price - self.sale_price) / self.price) * 100
        return 0


class CartItem(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="cart_items"
    )
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.plant.price * self.quantity

    class Meta:
        unique_together = ["user", "plant"]


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
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    @property
    def subtotal(self):
        return self.quantity * self.price
