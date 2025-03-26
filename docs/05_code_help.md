# Write script for adding category and product located in store sub app, add example records to the database table in this django sqlite

in script/ in root

write script that first create some categoryes and than add some plant product in that categoryes

and this both model contain image field but for know not uploading image

## this are models

```python
class Category(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="category_images/")
    slug = models.SlugField(unique=True)
    # is_featured = models.BooleanField(default=False)


class Product(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    image = models.ImageField(upload_to="product_images/", default=False)
    description = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
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

    inventory = models.PositiveIntegerField(default=0)

    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def discount_percentage(self):
        if self.sale_price:
            return ((self.price - self.sale_price) / self.price) * 100
        return 0
```

add this is project tree

```plaintext
.
├── docs
├── scripts
├── src
│   ├── apps
│   │   ├── account
│   │   ├── core
│   │   ├── store < product and category models are here
│   │   ├── tags
│   ├── logs
│   ├── media
│   ├── node_modules
│   ├── project
│   │   └── settings
│   ├── static
│   │   ├── css
│   │   ├── images < you can use this images
│   │   ├── js
│   │   ├── src
│   │   └── videos
│   └── templates
│       ├── account
│       ├── components
│       ├── core
│       └── store
└── tests
```
