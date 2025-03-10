import os

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from ....store.models import Category, Plant, Tag  # Adjust the import as necessary


class Command(BaseCommand):
    help = "Populates the database with categories and plants"

    def handle(self, *args, **kwargs):
        self.populate_database()

    def populate_database(self):
        print("Starting database population...")
        self.create_categories()
        self.create_tags()
        self.create_plants()
        print("Database population complete!")

    def create_categories(self):
        category_data = [
            {
                "title": "Indoor Plants",
                "description": "Beautiful plants to brighten up your indoor spaces. Perfect for adding a touch of greenery to your home or office.",
                "image": "images/product_category/Aloe_Vera.jpeg",  # Updated image
            },
            {
                "title": "Outdoor Plants",
                "description": "Hardy plants ideal for your garden, patio, or balcony. Enhance your outdoor space with vibrant colors and textures.",
                "image": "images/product_category/Rose_Bush.jpeg",  # Updated image
            },
            {
                "title": "Succulents",
                "description": "Low-maintenance and drought-tolerant succulents. A variety of shapes and colors for any small space or collection.",
                "image": "images/product_category/Echeveria.jpeg",  # Updated image
            },
            {
                "title": "Fruit Plants",
                "description": "Delicious fruit-bearing plants you can grow at home. Enjoy fresh, homegrown fruits right from your garden or balcony.",
                "image": "images/product_category/Apple_Tree.jpeg",  # Added category and image
            },
            {
                "title": "Flavor Plants",
                "description": "Aromatic herbs and flavorful plants to enhance your culinary creations. Grow your own spices and seasonings for fresh, delicious meals.",
                "image": "images/product_category/Basil.webp",  # Added category and image
            },
            {
                "title": "Medicinal Plants of India",
                "description": "Plants like Tulsi (Holy Basil) and Neem known for their medicinal properties and used in traditional Ayurvedic practices.",
                "image": "images/product_category/Tulsi.jpeg",  # Updated image
            },
            {
                "title": "Desert Plants of Rajasthan",
                "description": "Plants such as Cactus and Desert Rose that thrive in the harsh conditions of the Thar Desert, showcasing unique adaptations.",
                "image": "images/product_category/Cactus.jpeg",  # Updated image
            },
        ]

        for data in category_data:
            slug = slugify(data["title"])
            if Category.objects.filter(slug=slug).exists():
                print(f"Category '{data['title']}' already exists. Skipping.")
                continue

            category = Category(
                title=data["title"], description=data["description"], slug=slug
            )
            self.handle_image_upload(category, data["image"])
            category.save()
            print(f"Category '{data['title']}' added successfully.")

    def handle_image_upload(self, instance, image_path):
        """
        Handles uploading an image from the static directory to the model's image field.
        """
        full_image_path = os.path.join(settings.BASE_DIR, "static", image_path)

        if not os.path.exists(full_image_path):
            print(f"Image file not found: {full_image_path}")
            return

        try:
            with open(full_image_path, "rb") as f:
                instance.image.save(os.path.basename(image_path), File(f), save=False)
            print(f"Image '{image_path}' uploaded successfully for '{instance.title}'.")
        except Exception as e:
            print(f"Error uploading image for '{instance.title}': {e}")

    def create_tags(self):
        tag_data = [
            "Low Maintenance",
            "Pet Friendly",
            "Air Purifying",
            "Easy Care",
            "Drought Tolerant",
        ]

        for tag_name in tag_data:
            tag, created = Tag.objects.get_or_create(
                tag=tag_name, slug=slugify(tag_name)
            )
            if created:
                print(f"Tag '{tag_name}' created.")
            else:
                print(f"Tag '{tag_name}' already exists.")

    def create_plants(self):
        plant_data = [
            {
                "title": "ZZ Plant",
                "category": "Indoor Plants",
                "description": "A low-maintenance plant that thrives in low light and dry conditions.",
                "price": 1700.00,
                "scientific_name": "Zamioculcas zamiifolia",
                "care_difficulty": "EASY",
                "sunlight_requirements": "LOW_LIGHT",
                "water_frequency": "LOW",
                "inventory": 50,
                "tags": ["Low Maintenance", "Drought Tolerant"],
                "image": "images/product_category/zz_plant.webp",
            },
            {
                "title": "Aloe Vera",
                "category": "Indoor Plants",
                "description": "Aloe Vera is known for its healing properties and thrives in dry conditions.",
                "price": 1199.00,
                "scientific_name": "Aloe barbadensis miller",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 60,
                "tags": ["Medicinal", "Drought Tolerant"],
                "image": "images/product_category/Aloe_Vera.jpeg",
            },
            {
                "title": "Snake Plant",
                "category": "Indoor Plants",
                "description": "A hardy plant that purifies the air and is very low-maintenance.",
                "price": 1500.00,
                "scientific_name": "",
                "care_difficulty": "EASY",
                "sunlight_requirements": "LOW_LIGHT",
                "water_frequency": "LOW",
                "inventory": 45,
                "tags": ["Air Purifying", "Low Maintenance"],
                "image": "images/product_category/Snake_Plant.jpeg",
            },
            {
                "title": "Pothos",
                "category": "Indoor Plants",
                "description": "A popular and easy-to-grow plant known for its trailing vines.",
                "price": 999.00,
                "scientific_name": "Epipremnum aureum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 55,
                "tags": ["Trailing Plant", "Easy to Grow"],
                "image": "images/product_category/Pothos.webp",
            },
            {
                "title": "Spider Plant",
                "category": "Indoor Plants",
                "description": "A classic houseplant that produces 'spiderettes' or baby plants.",
                "price": 850.00,
                "scientific_name": "Chlorophytum comosum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 65,
                "tags": ["Air Purifying", "Easy to Propagate"],
                "image": "images/product_category/Spider_Plant.webp",
            },
            {
                "title": "Jade Plant",
                "category": "Indoor Plants",
                "description": "A succulent that symbolizes good luck and prosperity.",
                "price": 1350.00,
                "scientific_name": "Crassula ovata",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 40,
                "tags": ["Succulent", "Good Luck"],
                "image": "images/product_category/Jade_Plant.jpeg",
            },
            # Category: Outdoor Plants
            {
                "title": "Rose Bush",
                "category": "Outdoor Plants",
                "description": "A classic flowering bush that adds beauty and fragrance to your garden.",
                "price": 1800.00,
                "scientific_name": "Rosa spp.",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 55,
                "tags": ["Flowering", "Fragrant"],
                "image": "images/product_category/Rose_Bush.jpeg",
            },
            {
                "title": "Lavender",
                "category": "Outdoor Plants",
                "description": "A fragrant herb that attracts pollinators and thrives in full sun.",
                "price": 950.00,
                "scientific_name": "Lavandula angustifolia",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 50,
                "tags": ["Fragrant", "Herb"],
                "image": "images/product_category/Lavender.webp",
            },
            {
                "title": "Marigold",
                "category": "Outdoor Plants",
                "description": "Vibrant, easy-to-grow flowers that bring color and joy to any garden.",
                "price": 500.00,
                "scientific_name": "Tagetes spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 100,
                "tags": ["Flowering", "Colorful"],
                "image": "images/product_category/Marigold.jpeg",
            },
            {
                "title": "Tulip",
                "category": "Outdoor Plants",
                "description": "Bright and beautiful flowers that add elegance to any garden.",
                "price": 1200.00,
                "scientific_name": "Tulipa spp.",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 70,
                "tags": ["Flowering", "Colorful"],
                "image": "images/product_category/Tulip.jpg",
            },
            {
                "title": "Sunflower",
                "category": "Outdoor Plants",
                "description": "Tall, bright flowers that bring sunshine to your garden.",
                "price": 600.00,
                "scientific_name": "Helianthus annuus",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "HIGH",
                "inventory": 80,
                "tags": ["Flowering", "Colorful"],
                "image": "images/product_category/Sunflower.jpeg",
            },
            {
                "title": "Jasmine",
                "category": "Outdoor Plants",
                "description": "A fragrant vine plant that adds elegance to outdoor spaces.",
                "price": 1500.00,
                "scientific_name": "Jasminum spp.",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 60,
                "tags": ["Fragrant", "Vine"],
                "image": "images/product_category/Jasmine.jpeg",
            },
            {
                "title": "Echeveria",
                "category": "Succulents",
                "description": "A beautiful rosette-shaped succulent with a variety of colors.",
                "price": 800.00,
                "scientific_name": "Echeveria spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 90,
                "tags": ["Low Maintenance", "Colorful"],
                "image": "images/product_category/Echeveria.jpeg",
            },
            {
                "title": "Aloe Vera",
                "category": "Succulents",
                "description": "A hardy succulent known for its healing properties.",
                "price": 950.00,
                "scientific_name": "Aloe barbadensis miller",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 80,
                "tags": ["Medicinal", "Low Maintenance"],
                "image": "images/product_category/Aloe_Vera.jpeg",
            },
            {
                "title": "Jade Plant",
                "category": "Succulents",
                "description": "A classic succulent known for its rounded, fleshy leaves.",
                "price": 1200.00,
                "scientific_name": "Crassula ovata",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 85,
                "tags": ["Low Maintenance", "Hardy"],
                "image": "images/product_category/Jade_Plant.jpeg",
            },
            {
                "title": "Sedum",
                "category": "Succulents",
                "description": "A low-maintenance, drought-tolerant succulent with vibrant colors.",
                "price": 700.00,
                "scientific_name": "Sedum spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 60,
                "tags": ["Low Maintenance", "Drought Tolerant"],
                "image": "images/product_category/Sedum.jpeg",
            },
            {
                "title": "Cactus",
                "category": "Succulents",
                "description": "A hardy, drought-tolerant plant with a variety of shapes.",
                "price": 850.00,
                "scientific_name": "Cactaceae",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 75,
                "tags": ["Low Maintenance", "Drought Tolerant"],
                "image": "images/product_category/Cactus.jpeg",
            },
            {
                "title": "Crassula",
                "category": "Succulents",
                "description": "A resilient succulent with thick, glossy leaves.",
                "price": 950.00,
                "scientific_name": "Crassula spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 65,
                "tags": ["Low Maintenance", "Hardy"],
                "image": "images/product_category/Crassula.webp",
            },
            # Category: Fruit Plants
            {
                "title": "Tomato Plant",
                "category": "Fruit Plants",
                "description": "Homegrown tomatoes are a flavorful addition to any garden.",
                "price": 800.00,
                "scientific_name": "Solanum lycopersicum",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 50,
                "tags": ["Fruit Bearing", "Vegetable"],
                "image": "images/product_category/Tomato_Plant.jpg",
            },
            {
                "title": "Strawberry Plant",
                "category": "Fruit Plants",
                "description": "Fresh, sweet strawberries that can be grown at home.",
                "price": 500.00,
                "scientific_name": "Fragaria × ananassa",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 70,
                "tags": ["Fruit Bearing", "Low Maintenance"],
                "image": "images/product_category/Strawberry_Plant.jpeg",
            },
            {
                "title": "Apple Tree",
                "category": "Fruit Plants",
                "description": "A classic fruit tree that produces delicious apples.",
                "price": 2500.00,
                "scientific_name": "Malus domestica",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 40,
                "tags": ["Fruit Bearing", "Tree"],
                "image": "images/product_category/Apple_Tree.jpeg",
            },
            {
                "title": "Lemon Tree",
                "category": "Fruit Plants",
                "description": "A refreshing citrus tree that can thrive in pots or gardens.",
                "price": 2000.00,
                "scientific_name": "Citrus limon",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 60,
                "tags": ["Fruit Bearing", "Citrus"],
                "image": "images/product_category/Lemon_Tree.jpeg",
            },
            {
                "title": "Guava Tree",
                "category": "Fruit Plants",
                "description": "A tropical fruit tree that produces sweet guavas.",
                "price": 1500.00,
                "scientific_name": "Psidium guajava",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 50,
                "tags": ["Fruit Bearing", "Tropical"],
                "image": "images/product_category/Guava_Tree.webp",
            },
            {
                "title": "Papaya Tree",
                "category": "Fruit Plants",
                "description": "A fast-growing tree that produces delicious, tropical papayas.",
                "price": 1200.00,
                "scientific_name": "Carica papaya",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "HIGH",
                "inventory": 55,
                "tags": ["Fruit Bearing", "Tropical"],
                "image": "images/product_category/Papaya_Tree.jpeg",
            },
            # Category: Flavor Plants
            {
                "title": "Basil",
                "category": "Flavor Plants",
                "description": "A fragrant herb commonly used in culinary dishes.",
                "price": 300.00,
                "scientific_name": "Ocimum basilicum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 100,
                "tags": ["Herb", "Culinary"],
                "image": "images/product_category/Basil.webp",
            },
            {
                "title": "Mint",
                "category": "Flavor Plants",
                "description": "A fresh herb that adds a burst of flavor to various dishes and drinks.",
                "price": 350.00,
                "scientific_name": "Mentha spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 95,
                "tags": ["Herb", "Culinary"],
                "image": "images/product_category/Mint.jpeg",
            },
            {
                "title": "Thyme",
                "category": "Flavor Plants",
                "description": "An aromatic herb used to flavor many dishes.",
                "price": 450.00,
                "scientific_name": "Thymus vulgaris",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 90,
                "tags": ["Herb", "Culinary"],
                "image": "images/product_category/thyme-herb-scaled.webp",
            },
            {
                "title": "Rosemary",
                "category": "Flavor Plants",
                "description": "A fragrant herb used in many savory dishes.",
                "price": 500.00,
                "scientific_name": "Rosmarinus officinalis",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 80,
                "tags": ["Herb", "Culinary"],
                "image": "images/product_category/Rosemary.jpeg",
            },
            {
                "title": "Oregano",
                "category": "Flavor Plants",
                "description": "A flavorful herb often used in Mediterranean cuisine.",
                "price": 400.00,
                "scientific_name": "Origanum vulgare",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 85,
                "tags": ["Herb", "Culinary"],
                "image": "images/product_category/Oregano.jpg",
            },
            {
                "title": "Coriander",
                "category": "Flavor Plants",
                "description": "A herb with both leaves and seeds used in cooking.",
                "price": 350.00,
                "scientific_name": "Coriandrum sativum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 90,
                "tags": ["Herb", "Culinary"],
                "image": "images/product_category/Coriander.jpeg",
            },
            # Category: Medicinal Plants of India
            {
                "title": "Tulsi",
                "category": "Medicinal Plants of India",
                "description": "A sacred plant in Ayurveda, known for its medicinal and spiritual significance.",
                "price": 700.00,
                "scientific_name": "Ocimum sanctum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 100,
                "tags": ["Medicinal", "Sacred"],
                "image": "images/product_category/Tulsi.jpeg",
            },
            {
                "title": "Neem",
                "category": "Medicinal Plants of India",
                "description": "Known for its antibacterial and anti-inflammatory properties.",
                "price": 1100.00,
                "scientific_name": "Azadirachta indica",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 80,
                "tags": ["Medicinal", "Herbal"],
                "image": "images/product_category/neem_plant.jpg",
            },
            {
                "title": "Ashwagandha",
                "category": "Medicinal Plants of India",
                "description": "Used for stress relief and immunity boosting.",
                "price": 1200.00,
                "scientific_name": "Withania somnifera",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "LOW",
                "inventory": 70,
                "tags": ["Medicinal", "Herbal"],
                "image": "images/product_category/Ashwagandha.jpeg",
            },
            {
                "title": "Moringa",
                "category": "Medicinal Plants of India",
                "description": "Known as the 'Miracle Tree' for its nutrient-rich leaves.",
                "price": 900.00,
                "scientific_name": "Moringa oleifera",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 65,
                "tags": ["Medicinal", "Superfood"],
                "image": "images/product_category/Moringa.jpeg",
            },
            {
                "title": "Giloy",
                "category": "Medicinal Plants of India",
                "description": "A potent herb for boosting immunity.",
                "price": 800.00,
                "scientific_name": "Tinospora cordifolia",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 60,
                "tags": ["Medicinal", "Immunity Boost"],
                "image": "images/product_category/Giloy.jpeg",
            },
            {
                "title": "Brahmi",
                "category": "Medicinal Plants of India",
                "description": "A herb known for its cognitive and memory-enhancing properties.",
                "price": 850.00,
                "scientific_name": "Bacopa monnieri",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 75,
                "tags": ["Medicinal", "Cognitive Enhancement"],
                "image": "images/product_category/Brahmi.webp",
            },
            # Category: Desert Plants of Rajasthan
            {
                "title": "Cactus",
                "category": "Desert Plants of Rajasthan",
                "description": "A hardy desert plant with a variety of shapes.",
                "price": 750.00,
                "scientific_name": "Cactaceae",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 85,
                "tags": ["Desert", "Drought Tolerant"],
                "image": "images/product_category/Cactus.jpeg",
            },
            {
                "title": "Desert Rose",
                "category": "Desert Plants of Rajasthan",
                "description": "A beautiful flowering plant that thrives in dry conditions.",
                "price": 950.00,
                "scientific_name": "Adenium obesum",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 60,
                "tags": ["Flowering", "Drought Tolerant"],
                "image": "images/product_category/Desert_Rose.jpeg",
            },
            {
                "title": "Agave",
                "category": "Desert Plants of Rajasthan",
                "description": "A tough desert plant that stores water in its leaves.",
                "price": 1100.00,
                "scientific_name": "Agave americana",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 75,
                "tags": ["Desert", "Water-Storing"],
                "image": "images/product_category/Agave.jpg",
            },
            {
                "title": "Aloe Vera",
                "category": "Desert Plants of Rajasthan",
                "description": "Known for its medicinal properties, Aloe thrives in arid conditions.",
                "price": 800.00,
                "scientific_name": "Aloe barbadensis miller",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 60,
                "tags": ["Desert", "Medicinal"],
                "image": "images/product_category/Aloe_Vera.jpeg",
            },
            {
                "title": "Brittle Bush",
                "category": "Desert Plants of Rajasthan",
                "description": "A resilient desert plant with beautiful yellow flowers.",
                "price": 700.00,
                "scientific_name": "Encelia farinosa",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 50,
                "tags": ["Desert", "Flowering"],
                "image": "images/product_category/brittlebush1.jpg",
            },
            {
                "title": "Ocotillo",
                "category": "Desert Plants of Rajasthan",
                "description": "A striking desert plant that produces vibrant red flowers in the spring.",
                "price": 1000.00,
                "scientific_name": "Fouquieria splendens",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 40,
                "tags": ["Desert", "Flowering"],
                "image": "images/product_category/Ocotillo.webp",
            },
        ]

        for data in plant_data:
            try:
                category = Category.objects.get(title=data["category"])
            except Category.DoesNotExist:
                print(
                    f"Category '{data['category']}' does not exist. Skipping plant '{data['title']}'."
                )
                continue

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
            )

            self.handle_image_upload(plant, data["image"])
            plant.save()

            for tag_name in data["tags"]:
                try:
                    tag = Tag.objects.get(tag=tag_name)
                    plant.tags.add(tag)
                    print(f"Tag '{tag_name}' added to plant '{data['title']}'.")
                except Tag.DoesNotExist:
                    print(f"Tag '{tag_name}' does not exist. Skipping.")

            print(f"Plant '{data['title']}' added successfully.")
