import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from ....store.models import Category, Plant, Tag


class Command(BaseCommand):
    help = "Populates the database with categories and plants"

    def handle(self, *args, **kwargs):
        self.populate_database()

    def populate_database(self):
        """
        Populates the database with sample categories and plants.
        """

        print("Starting database population...")

        # 1. Create Categories
        category_data = [
            {
                "title": "Indoor Plants",
                "description": "Beautiful plants to brighten up your indoor space.",
                "image": "images/buldinginplant.png",  # Relative path to image in static/images
            },
            {
                "title": "Outdoor Plants",
                "description": "Hardy plants perfect for your garden.",
                "image": "images/ecosystem-restoration.jpg",
            },
            {
                "title": "Succulents",
                "description": "Low-maintenance and drought-tolerant succulents.",
                "image": "images/urban-living.jpg",
            },
        ]

        categories = []
        for data in category_data:
            # Create slug from title
            slug = slugify(data["title"])

            # Check if category already exists
            if Category.objects.filter(slug=slug).exists():
                print(f"Category '{data['title']}' already exists. Skipping.")
                continue

            category = Category(
                title=data["title"], description=data["description"], slug=slug
            )

            # Handle Image (assuming images are in static/images)
            image_path = os.path.join(settings.BASE_DIR, "static", data["image"])
            try:
                with open(image_path, "rb") as f:  # Open the image in binary read mode
                    category.image.save(
                        os.path.basename(data["image"]), File(f), save=False
                    )  # save=False to prevent premature saving
                print(f"Image '{data['image']}' loaded for category '{data['title']}'")
            except FileNotFoundError:
                print(f"Image file not found: {image_path}")
            except Exception as e:
                print(f"Error loading image for category '{data['title']}': {e}")
            categories.append(category)

        Category.objects.bulk_create(categories)

        # Now save the categories to persist the images
        for category in categories:
            category.save()
        print("Categories added successfully.")

        # 2. Create Tags (example)
        tag_data = [
            "Low Maintenance",
            "Pet Friendly",
            "Air Purifying",
            "Easy Care",
            "Drought Tolerant",
        ]
        tags = []
        for tag_name in tag_data:
            # Create the tag, slugify the name for the slug
            tag, created = Tag.objects.get_or_create(
                tag=tag_name, slug=slugify(tag_name)
            )
            tags.append(tag)
        print("Tags added successfully.")

        # 3. Create Plants
        plant_data = [
            {
                "title": "Aloe Vera",
                "category": "Indoor Plants",
                "description": "Aloe Vera is a succulent plant with soothing properties.",
                "price": 15.99,
                "scientific_name": "Aloe barbadensis miller",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "LOW",
                "inventory": 100,
                "tags": ["Low Maintenance", "Air Purifying"],
                "image": "images/aloe-vera.jpg",
            },
            {
                "title": "Cactus",
                "category": "Succulents",
                "description": "Cactus plants are perfect for dry environments.",
                "price": 12.49,
                "scientific_name": "Cactaceae",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 80,
                "tags": ["Low Maintenance", "Drought Tolerant"],
                "image": "images/cactus.jpg",
            },
        ]

        for data in plant_data:
            # Get the category object
            category = Category.objects.get(title=data["category"])

            # Create the plant
            plant = Plant(
                title=data["title"],
                category=category,
                description=data["description"],
                price=data["price"],
                scientific_name=data.get("scientific_name"),
                care_difficulty=data["care_difficulty"],
                sunlight_requirements=data["sunlight_requirements"],
                water_frequency=data["water_frequency"],
                inventory=data["inventory"],
                sale_price=data.get("sale_price"),
            )

            # Handle plant image
            image_path = os.path.join(settings.BASE_DIR, "static", data["image"])
            try:
                with open(image_path, "rb") as f:
                    plant.image.save(
                        os.path.basename(data["image"]), File(f), save=False
                    )  # save=False
                print(f"Image '{data['image']}' loaded for plant '{data['title']}'")
            except FileNotFoundError:
                print(f"Image file not found: {image_path}")
            except Exception as e:
                print(f"Error loading image for plant '{data['title']}': {e}")

            plant.save()  # Save the plant first (and the image)

            # Add tags (after the plant is saved)
            for tag_name in data["tags"]:
                tag = Tag.objects.get(tag=tag_name)  # Use the 'tag' field for lookup
                plant.tags.add(tag)

            print(f"Plant '{data['title']}' added successfully.")

        print("Database population complete!")

        # 4. Display All Categories and Plants
        print("\n--- All Categories ---")
        categories = Category.objects.all()
        for category in categories:
            print(
                f"Category: {category.title} | Slug: {category.slug} | Description: {category.description}"
            )

        print("\n--- All Plants ---")
        plants = Plant.objects.all()
        for plant in plants:
            print(
                f"Plant: {plant.title} | Category: {plant.category.title} | Price: {plant.price} | Tags: {', '.join([tag.tag for tag in plant.tags.all()])}"
            )
