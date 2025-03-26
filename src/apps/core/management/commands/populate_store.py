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
                "image": "images/categories/indoor_plants.jpg",
            },
            {
                "title": "Outdoor Plants",
                "description": "Hardy plants ideal for your garden, patio, or balcony. Enhance your outdoor space with vibrant colors and textures.",
                "image": "images/categories/outdoor_plants.jpg",
            },
            {
                "title": "Succulents",
                "description": "Low-maintenance and drought-tolerant succulents. A variety of shapes and colors for any small space or collection.",
                "image": "images/categories/succulents.jpg",
            },
            {
                "title": "Fruit Plants",
                "description": "Delicious fruit-bearing plants you can grow at home. Enjoy fresh, homegrown fruits right from your garden or balcony.",
                "image": "images/categories/fruits.jpeg",
            },
            {
                "title": "Flavor Plants",
                "description": "Aromatic herbs and flavorful plants to enhance your culinary creations. Grow your own spices and seasonings for fresh, delicious meals.",
                "image": "images/categories/flavor.jpg",
            },
            {
                "title": "Medicinal Plants of India",
                "description": "Plants like Tulsi (Holy Basil) and Neem known for their medicinal properties and used in traditional Ayurvedic practices.",
                "image": "images/categories/medicinal_plants_of_india.jpg",
            },
            {
                "title": "Desert Plants of Rajasthan",
                "description": "Plants such as Cactus and Desert Rose that thrive in the harsh conditions of the Thar Desert, showcasing unique adaptations.",
                "image": "images/categories/desert_plants_of_rajasthan.jpg",
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
                "description": "The ZZ Plant is a resilient, low-maintenance indoor plant ideal for beginners. It thrives in low light and dry conditions, making it perfect for homes and offices. Its glossy, dark green leaves add a touch of elegance to any space, and it requires minimal care to flourish.",
                "price": 1700.00,
                "scientific_name": "Zamioculcas zamiifolia",
                "care_difficulty": "EASY",
                "sunlight_requirements": "LOW_LIGHT",
                "water_frequency": "LOW",
                "inventory": 50,
                "tags": ["Low Maintenance", "Drought Tolerant"],
                "image": "images/plants/zz_plant.jpg",
            },
            {
                "title": "Aloe Vera",
                "category": "Indoor Plants",
                "description": "Aloe Vera is a hardy succulent celebrated for its healing properties. It thrives in dry conditions and requires little water, making it an excellent choice for busy individuals. Its gel-filled leaves are widely used in skincare and medicinal applications.",
                "price": 1199.00,
                "scientific_name": "Aloe barbadensis miller",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 60,
                "tags": ["Medicinal", "Drought Tolerant"],
                "image": "images/plants/aloe_vera.jpg",
            },
            {
                "title": "Snake Plant",
                "category": "Indoor Plants",
                "description": "The Snake Plant is a hardy and air-purifying indoor plant that requires minimal care. Known for its upright, sword-like leaves, it thrives in low light and is drought-tolerant, making it a favorite among plant enthusiasts.",
                "price": 1500.00,
                "scientific_name": "",
                "care_difficulty": "EASY",
                "sunlight_requirements": "LOW_LIGHT",
                "water_frequency": "LOW",
                "inventory": 45,
                "tags": ["Air Purifying", "Low Maintenance"],
                "image": "images/plants/snake_plant.jpg",
            },
            {
                "title": "Pothos",
                "category": "Indoor Plants",
                "description": "A popular and easy-to-grow plant known for its trailing vines. It adapts well to various lighting conditions and is perfect for hanging baskets or climbing trellises.",
                "price": 999.00,
                "scientific_name": "Epipremnum aureum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 55,
                "tags": ["Trailing Plant", "Easy to Grow"],
                "image": "images/plants/pothos.webp",
            },
            {
                "title": "Spider Plant",
                "category": "Indoor Plants",
                "description": "A classic houseplant that produces 'spiderettes' or baby plants. It is known for its air-purifying qualities and thrives in a variety of indoor environments.",
                "price": 850.00,
                "scientific_name": "Chlorophytum comosum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 65,
                "tags": ["Air Purifying", "Easy to Propagate"],
                "image": "images/plants/spider_plant.webp",
            },
            {
                "title": "Jade Plant",
                "category": "Indoor Plants",
                "description": "A succulent that symbolizes good luck and prosperity. It is a low-maintenance plant with thick, fleshy leaves that thrive in sunny locations.",
                "price": 1350.00,
                "scientific_name": "Crassula ovata",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 40,
                "tags": ["Succulent", "Good Luck"],
                "image": "images/plants/jade_plant.jpg",
            },
            # Category: Outdoor Plants
            {
                "title": "Rose Bush",
                "category": "Outdoor Plants",
                "description": "Rose bushes are a timeless addition to any garden, celebrated for their exquisite blooms and enchanting fragrance, bringing romance and elegance to outdoor spaces. These classic flowering shrubs produce a stunning array of colors and varieties, requiring regular pruning and care to thrive, rewarding gardeners with a continuous display of beauty throughout the growing season.",
                "price": 1800.00,
                "scientific_name": "Rosa spp.",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 55,
                "tags": ["Flowering", "Fragrant"],
                "image": "images/plants/rose_bush.jpeg",
            },
            {
                "title": "Lavender",
                "category": "Outdoor Plants",
                "description": "A highly aromatic herb known for its relaxing scent and beautiful purple flowers. It's a favorite among gardeners and pollinators alike. This fragrant herb attracts pollinators and thrives in full sun, requiring only low watering.",
                "price": 950.00,
                "scientific_name": "Lavandula angustifolia",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 50,
                "tags": ["Fragrant", "Herb"],
                "image": "images/plants/lavender.jpg",
            },
            {
                "title": "Marigold",
                "category": "Outdoor Plants",
                "description": "Cheerful and easy-to-grow flowers that add a burst of color to any garden. They are known for their ability to deter pests and attract beneficial insects. These vibrant flowers bring color and joy to any garden and are incredibly easy to grow.",
                "price": 500.00,
                "scientific_name": "Tagetes spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 100,
                "tags": ["Flowering", "Colorful"],
                "image": "images/plants/merigold.jpg",
            },
            {
                "title": "Tulip",
                "category": "Outdoor Plants",
                "description": "Tulips herald the arrival of spring with their cup-shaped blossoms and vibrant colors. These bulbs are perfect for adding a splash of elegance to gardens and landscapes, blooming in an array of hues and forms.",
                "price": 1200.00,
                "scientific_name": "Tulipa spp.",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 70,
                "tags": ["Flowering", "Colorful"],
                "image": "images/plants/tulip.jpg",
            },
            {
                "title": "Sunflower",
                "category": "Outdoor Plants",
                "description": "Sunflowers are known for their towering height and vibrant yellow petals, embodying the warmth of summer. These iconic flowers not only brighten gardens but also attract pollinators and provide seeds for wildlife.",
                "price": 600.00,
                "scientific_name": "Helianthus annuus",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "HIGH",
                "inventory": 80,
                "tags": ["Flowering", "Colorful"],
                "image": "images/plants/sunflower.jpg",
            },
            {
                "title": "Jasmine",
                "category": "Outdoor Plants",
                "description": "Jasmine is celebrated for its intensely fragrant flowers that perfume the evening air. This climbing vine is ideal for adorning trellises and walls, adding a touch of romance and elegance to outdoor spaces.",
                "price": 1500.00,
                "scientific_name": "Jasminum spp.",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MODERATE",
                "inventory": 60,
                "tags": ["Fragrant", "Vine"],
                "image": "images/plants/jasmine.jpg",
            },
            {
                "title": "Echeveria",
                "category": "Succulents",
                "description": "Echeverias are prized for their stunning rosette-shaped arrangements of leaves, creating living art in gardens and containers. These succulents come in a spectrum of colors and textures, offering endless possibilities for creative displays.",
                "price": 800.00,
                "scientific_name": "Echeveria spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 90,
                "tags": ["Low Maintenance", "Colorful"],
                "image": "images/plants/echeveria.jpeg",
            },
            {
                "title": "Aloe Vera",
                "category": "Succulents",
                "description": "Aloe Vera is a hardy succulent celebrated for its healing properties, making it a popular choice for homes. It thrives in dry conditions and requires little water, making it an excellent choice for busy individuals. Its gel-filled leaves are widely used in skincare and medicinal applications.",
                "price": 950.00,
                "scientific_name": "Aloe barbadensis miller",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 80,
                "tags": ["Medicinal", "Low Maintenance"],
                "image": "images/plants/aloe_vera.jpg",
            },
            {
                "title": "Jade Plant",
                "category": "Succulents",
                "description": "The Jade Plant is a succulent symbolizing good luck and prosperity, making it a thoughtful gift. Known for its thick, fleshy leaves and tree-like appearance, it is a popular houseplant that thrives with minimal care and bright sunlight.",
                "price": 1200.00,
                "scientific_name": "Crassula ovata",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 85,
                "tags": ["Low Maintenance", "Hardy"],
                "image": "images/plants/jade_plant.jpeg",
            },
            {
                "title": "Sedum",
                "category": "Succulents",
                "description": "Sedums are low-maintenance succulents that offer a variety of colors and textures to gardens and containers. These drought-tolerant plants are perfect for adding visual interest to rock gardens or green roofs.",
                "price": 700.00,
                "scientific_name": "Sedum spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 60,
                "tags": ["Low Maintenance", "Drought Tolerant"],
                "image": "images/plants/sedum.jpeg",
            },
            {
                "title": "Cactus",
                "category": "Succulents",
                "description": "Cacti are iconic desert plants, celebrated for their resilience and unique adaptations to arid environments, adding a touch of the exotic to any collection. These hardy plants come in a stunning variety of shapes and sizes, requiring minimal care and thriving in sunny locations, making them perfect for both indoor and outdoor spaces.",
                "price": 750.00,
                "scientific_name": "Cactaceae",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 75,
                "tags": ["Low Maintenance", "Drought Tolerant"],
                "image": "images/plants/cactus.jpg",
            },
            {
                "title": "Crassula",
                "category": "Succulents",
                "description": "Crassula are resilient succulents, admired for their thick, glossy leaves and easy-care nature, making them a popular choice for both beginner and experienced plant enthusiasts. These hardy plants come in a variety of shapes and sizes, requiring minimal watering and thriving in bright, sunny locations, adding a touch of greenery and texture to any indoor or outdoor space.",
                "price": 950.00,
                "scientific_name": "Crassula spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 65,
                "tags": ["Low Maintenance", "Hardy"],
                "image": "images/plants/crassula.webp",
            },
            # Category: Fruit Plants
            {
                "title": "Tomato Plant",
                "category": "Fruit Plants",
                "description": "Homegrown tomatoes are a flavorful addition to any garden. Enjoy the taste of fresh, juicy tomatoes straight from your backyard. These plants thrive in sunny locations and require regular watering for best fruit production.",
                "price": 800.00,
                "scientific_name": "Solanum lycopersicum",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 50,
                "tags": ["Fruit Bearing", "Vegetable"],
                "image": "images/plants/tomato_plant.jpg",
            },
            {
                "title": "Strawberry Plant",
                "category": "Fruit Plants",
                "description": "Fresh, sweet strawberries that can be grown at home are a delightful treat. These plants are relatively easy to care for and produce delicious berries perfect for snacks, desserts, and jams.",
                "price": 500.00,
                "scientific_name": "Fragaria × ananassa",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 70,
                "tags": ["Fruit Bearing", "Low Maintenance"],
                "image": "images/plants/strawberry_plant.jpg",
            },
            {
                "title": "Apple Tree",
                "category": "Fruit Plants",
                "description": "A classic fruit tree that produces delicious apples, bringing the joy of orchard-fresh fruit to your home. These trees require some space and care, but the reward of homegrown apples is well worth the effort.",
                "price": 2500.00,
                "scientific_name": "Malus domestica",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 40,
                "tags": ["Fruit Bearing", "Tree"],
                "image": "images/plants/apple_tree.jpg",
            },
            {
                "title": "Lemon Tree",
                "category": "Fruit Plants",
                "description": "A lemon tree brings the bright, refreshing scent of citrus to your garden or patio, offering the joy of harvesting your own lemons for cooking, baking, and beverages. Imagine fresh lemonade made with lemons picked straight from your tree. These trees can thrive in pots and require plenty of sunlight and regular watering.",
                "price": 2000.00,
                "scientific_name": "Citrus limon",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 60,
                "tags": ["Fruit Bearing", "Citrus"],
                "image": "images/plants/lemon_tree.jpg",
            },
            {
                "title": "Guava Tree",
                "category": "Fruit Plants",
                "description": "A guava tree brings a taste of the tropics to your garden, offering the opportunity to harvest your own sweet and fragrant guavas. These trees are relatively easy to grow in warm climates and provide delicious fruit for fresh eating, jams, and desserts. Regular pruning and fertilization will encourage a bountiful harvest.",
                "price": 1500.00,
                "scientific_name": "Psidium guajava",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 50,
                "tags": ["Fruit Bearing", "Tropical"],
                "image": "images/plants/guava_tree.webp",
            },
            {
                "title": "Papaya Tree",
                "category": "Fruit Plants",
                "description": "A papaya tree offers the delight of harvesting your own sweet, tropical papayas at home, bringing an exotic touch to your garden. These fast-growing trees provide delicious fruit for breakfast, smoothies, and desserts. They thrive in warm climates with plenty of sunlight and regular watering.",
                "price": 1200.00,
                "scientific_name": "Carica papaya",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "HIGH",
                "inventory": 55,
                "tags": ["Fruit Bearing", "Tropical"],
                "image": "images/plants/papaya_tree.jpg",
            },
            # Category: Flavor Plants
            {
                "title": "Basil",
                "category": "Flavor Plants",
                "description": "Basil is a culinary staple, celebrated for its fragrant leaves and versatile use in dishes around the world. From pesto to salads, basil adds a distinctive, fresh flavor. This easy-to-grow herb thrives in sunny locations and rewards gardeners with a bountiful harvest throughout the summer.",
                "price": 300.00,
                "scientific_name": "Ocimum basilicum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 100,
                "tags": ["Herb", "Culinary"],
                "image": "images/plants/basil.jpeg",
            },
            {
                "title": "Mint",
                "category": "Flavor Plants",
                "description": "Mint is a refreshing herb known for its invigorating scent and cool flavor, perfect for teas, desserts, and savory dishes. Easy to grow and quick to spread, mint brings a burst of freshness to any garden or container. Regular harvesting encourages new growth and keeps this versatile herb at its best.",
                "price": 350.00,
                "scientific_name": "Mentha spp.",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 95,
                "tags": ["Herb", "Culinary"],
                "image": "images/plants/mint.jpeg",
            },
            {
                "title": "Thyme",
                "category": "Flavor Plants",
                "description": "Thyme is an aromatic herb with a distinctive earthy flavor, essential for seasoning a wide variety of dishes, from meats to vegetables. This low-growing herb is drought-tolerant and thrives in sunny locations, making it an easy and flavorful addition to any herb garden. Its small leaves pack a powerful flavor punch.",
                "price": 450.00,
                "scientific_name": "Thymus vulgaris",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 90,
                "tags": ["Herb", "Culinary"],
                "image": "images/plants/thyme.webp",
            },
            {
                "title": "Rosemary",
                "category": "Flavor Plants",
                "description": "Rosemary is an evergreen herb with a distinctive, piney aroma, perfect for flavoring meats, vegetables, and bread. This drought-tolerant plant thrives in sunny locations and requires minimal care, making it a flavorful and fragrant addition to any garden. Its woody stems and needle-like leaves add year-round interest.",
                "price": 500.00,
                "scientific_name": "Salvia rosmarinus",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 85,
                "tags": ["Herb", "Culinary", "Aromatic"],
                "image": "images/plants/rosemary.jpeg",
            },
            {
                "title": "Oregano",
                "category": "Flavor Plants",
                "description": "Oregano is a robust herb with a pungent, earthy flavor, essential for Italian and Mediterranean cuisine. This easy-to-grow herb thrives in sunny locations and requires minimal watering, making it a flavorful and low-maintenance addition to any herb garden. Its aromatic leaves add a distinctive zest to pizzas, pastas, and grilled meats.",
                "price": 380.00,
                "scientific_name": "Origanum vulgare",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 100,
                "tags": ["Herb", "Culinary"],
                "image": "images/plants/oregano.jpeg",
            },
            {
                "title": "Coriander",
                "category": "Flavor Plants",
                "description": "Coriander is a versatile herb, prized for both its vibrant leaves and aromatic seeds, enriching cuisines worldwide. Whether used fresh in salsas or ground as a spice, coriander adds a distinctive, zesty flavor. This easy-to-grow herb thrives in sunny locations and rewards gardeners with a bountiful harvest throughout the growing season.",
                "price": 350.00,
                "scientific_name": "Coriandrum sativum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 90,
                "tags": ["Herb", "Culinary"],
                "image": "images/plants/coriander.jpeg",
            },
            {
                "title": "Tulsi",
                "category": "Medicinal Plants of India",
                "description": "Tulsi, also known as Holy Basil, is revered in Ayurveda for its profound medicinal and spiritual properties, promoting overall well-being. This sacred plant is cherished for its ability to purify the environment, reduce stress, and boost immunity, making it a staple in traditional Indian households.",
                "price": 700.00,
                "scientific_name": "Ocimum sanctum",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 100,
                "tags": ["Medicinal", "Sacred"],
                "image": "images/plants/tulsi.jpeg",
            },
            {
                "title": "Neem",
                "category": "Medicinal Plants of India",
                "description": "Neem is celebrated for its potent antibacterial, antifungal, and anti-inflammatory properties, making it a cornerstone of traditional medicine. This versatile tree is used in skincare, dental hygiene, and natural remedies, offering a holistic approach to health and wellness. Its bitter leaves are a testament to its powerful medicinal benefits.",
                "price": 1100.00,
                "scientific_name": "Azadirachta indica",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 80,
                "tags": ["Medicinal", "Herbal"],
                "image": "images/plants/neem_plant.jpg",
            },
            {
                "title": "Ashwagandha",
                "category": "Medicinal Plants of India",
                "description": "Ashwagandha is revered for its adaptogenic properties, helping the body manage stress and boost immunity. This ancient herb is used to promote overall well-being, enhance cognitive function, and revitalize energy levels, making it a valuable addition to modern wellness routines.",
                "price": 1200.00,
                "scientific_name": "Withania somnifera",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "LOW",
                "inventory": 70,
                "tags": ["Medicinal", "Herbal"],
                "image": "images/plants/ashwagandha.jpeg",
            },
            {
                "title": "Moringa",
                "category": "Medicinal Plants of India",
                "description": "Moringa, often hailed as the 'Miracle Tree,' is celebrated for its exceptionally nutrient-rich leaves, providing a wide array of health benefits. This superfood is packed with vitamins, minerals, and antioxidants, supporting everything from immune function to healthy skin and hair, making it a versatile addition to any diet.",
                "price": 900.00,
                "scientific_name": "Moringa oleifera",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 65,
                "tags": ["Medicinal", "Superfood"],
                "image": "images/plants/moringa.jpeg",
            },
            {
                "title": "Giloy",
                "category": "Medicinal Plants of India",
                "description": "Giloy is a potent herb known for its remarkable ability to boost immunity and combat various infections, making it a cornerstone of Ayurvedic medicine. This powerful herb helps strengthen the body's natural defenses, promote detoxification, and improve overall vitality, ensuring a robust and resilient immune system.",
                "price": 800.00,
                "scientific_name": "Tinospora cordifolia",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 60,
                "tags": ["Medicinal", "Immunity Boost"],
                "image": "images/plants/giloy.jpeg",
            },
            {
                "title": "Brahmi",
                "category": "Medicinal Plants of India",
                "description": "Brahmi is revered in Ayurveda for its cognitive and memory-enhancing properties, making it a valuable herb for students and those seeking mental clarity. This traditional remedy supports brain function, reduces anxiety, and promotes overall mental well-being, ensuring a sharp and focused mind.",
                "price": 850.00,
                "scientific_name": "Bacopa monnieri",
                "care_difficulty": "EASY",
                "sunlight_requirements": "PARTIAL_SUN",
                "water_frequency": "MEDIUM",
                "inventory": 75,
                "tags": ["Medicinal", "Cognitive Enhancement"],
                "image": "images/plants/brahmi.webp",
            },
            # Category: Desert Plants of Rajasthan
            {
                "title": "Cactus",
                "category": "Desert Plants of Rajasthan",
                "description": "Cacti are iconic desert plants, celebrated for their resilience and unique adaptations to arid environments, adding a touch of the exotic to any collection. These hardy plants come in a stunning variety of shapes and sizes, requiring minimal care and thriving in sunny locations, making them perfect for both indoor and outdoor spaces.",
                "price": 750.00,
                "scientific_name": "Cactaceae",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 85,
                "tags": ["Desert", "Drought Tolerant"],
                "image": "images/plants/cactus.jpeg",
            },
            {
                "title": "Desert Rose",
                "category": "Desert Plants of Rajasthan",
                "description": "Desert Rose is a captivating flowering plant, prized for its stunning blooms and ability to thrive in dry conditions, adding a touch of elegance to arid landscapes. These resilient plants produce vibrant, trumpet-shaped flowers in a range of colors, requiring well-draining soil and plenty of sunlight, making them a striking addition to any desert-themed garden.",
                "price": 950.00,
                "scientific_name": "Adenium obesum",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 60,
                "tags": ["Flowering", "Drought Tolerant"],
                "image": "images/plants/desert_rose.jpg",
            },
            {
                "title": "Agave",
                "category": "Desert Plants of Rajasthan",
                "description": "Agave plants are striking succulents, renowned for their architectural form and drought tolerance, adding a bold statement to arid landscapes. These impressive plants store water efficiently in their thick, fleshy leaves, requiring minimal care and thriving in sunny locations, making them ideal for xeriscaping and adding a touch of desert drama to any garden.",
                "price": 1100.00,
                "scientific_name": "Agave americana",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 75,
                "tags": ["Desert", "Water-Storing"],
                "image": "images/plants/agave.jpg",
            },
            {
                "title": "Aloe Vera",
                "category": "Desert Plants of Rajasthan",
                "description": "Aloe Vera is a hardy succulent celebrated for its healing properties, making it a popular choice for homes. It thrives in dry conditions and requires little water, making it an excellent choice for busy individuals. Its gel-filled leaves are widely used in skincare and medicinal applications.",
                "price": 800.00,
                "scientific_name": "Aloe barbadensis miller",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 60,
                "tags": ["Desert", "Medicinal"],
                "image": "images/plants/aloe_vera.jpg",
            },
            {
                "title": "Brittle Bush",
                "category": "Desert Plants of Rajasthan",
                "description": "Brittle Bush is a resilient desert shrub, admired for its silvery foliage and cheerful yellow flowers, bringing a burst of color to arid landscapes. These drought-tolerant plants thrive in full sun and require minimal care, making them a valuable addition to desert gardens and xeriscaping projects. Their bright blooms attract pollinators, adding life and vibrancy to the desert environment.",
                "price": 700.00,
                "scientific_name": "Encelia farinosa",
                "care_difficulty": "EASY",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 50,
                "tags": ["Desert", "Flowering"],
                "image": "images/plants/brittlebush.jpg",
            },
            {
                "title": "Ocotillo",
                "category": "Desert Plants of Rajasthan",
                "description": "Ocotillo is a striking desert plant, celebrated for its spiny, whip-like stems and vibrant red flowers that bloom in the spring, adding a dramatic touch to arid landscapes. These unique plants require well-draining soil and plenty of sunlight, making them a captivating addition to desert gardens and xeriscaping projects. Their bright blooms attract hummingbirds, adding life and vibrancy to the desert environment.",
                "price": 1000.00,
                "scientific_name": "Fouquieria splendens",
                "care_difficulty": "MODERATE",
                "sunlight_requirements": "FULL_SUN",
                "water_frequency": "LOW",
                "inventory": 40,
                "tags": ["Desert", "Flowering"],
                "image": "images/plants/ocotillo.jpg",
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
