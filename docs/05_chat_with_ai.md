## GrowEarth: online plat store

project with django, sqllite, tailwind css, jinja template letes

### brand theme

primary: #a2a915;
secondary: #547131;
tertiary: #6c92b6;
saffron: #edc363;
darkBrown: #3f3929;

as my custom color tailwindcss config

### Home page of website

home.html with layout
{% extends '../layout.html' %}
{% load static %}
{% block title %}
Grow Earth: Cultivating Connection Through Plants
{% endblock %}
{% block content %}

<div class="bg-white">
  <!-- Hero Section: Impactful Introduction -->
  <section class="relative bg-primary/10 overflow-hidden min-h-screen">
    <!-- Background Video -->
    <div class="absolute inset-0 z-0">
      <video autoplay loop muted class="object-cover w-full h-full">
        <source src="{% static 'videos/output_background_video.mp4' %}" type="video/mp4" />
        Your browser does not support the video tag.
      </video>
    </div>

    <!-- Content with Blending Mode mix-blend-difference -->
    <div class="relative z-10 container mx-auto px-6 md:px-16 text-center py-24 md:py-36">
      <h1 class="text-5xl md:text-6xl font-bold leading-tight text-white">
        Nurturing Nature, One Plant at a Time 🌿
      </h1>
      <p class="text-lg md:text-xl mb-8 max-w-3xl mx-auto font-semibold text-white">
        Empowering communities and improving lives through sustainable plant
        care, bringing nature closer to you.
      </p>

      <!-- Buttons -->
      <div class="flex justify-center space-x-6">
        <a href="{% url 'store:categoryes' %}"
          class="bg-secondary text-white px-8 py-4 rounded-full hover:bg-secondary/90 transition duration-300 shadow-lg transform hover:scale-105">
          <i class="fas fa-seedling mr-2"></i> Start Growing Today
        </a>
        <a href="{% url 'core:mission' %}"
          class="border-2 border-tertiary text-tertiary px-8 py-4 rounded-full hover:bg-tertiary/10 transition duration-300 transform hover:scale-105">
          <i class="fab fa-envira mr-2"></i> Join Our Green Mission
        </a>
      </div>
    </div>

  </section>

  <!-- Our Impact: Plant's Role in the World -->
  <section class="container mx-auto py-24 px-4">
    <div class="text-center mb-12">
      <h2 class="text-3xl md:text-4xl font-bold text-secondary mb-4">
        How Plants Shape Our World 🌍
      </h2>
      <p class="text-lg text-darkBrown max-w-3xl mx-auto">
        Discover how plants positively impact our health, the ecosystem, and
        sustainability across the globe.
      </p>
    </div>

    <div class="grid md:grid-cols-3 gap-16">
      <!-- Mental Wellness -->
      <div class="p-8 text-center">
        <img src="{% static 'images/mental-wellness.jpg' %}" alt="Mental Wellness"
          class="w-full h-64 object-cover rounded-lg mb-6" />
        <h3 class="text-2xl font-semibold text-secondary mb-4">
          Mental & Physical Wellness 🌿
        </h3>
        <ul class="text-darkBrown text-left space-y-2 ml-8">
          <li><i class="fas fa-heartbeat mr-2"></i> Promote Mental Health</li>
          <li><i class="fas fa-lungs mr-2"></i> Improve Air Quality</li>
          <li><i class="fas fa-spa mr-2"></i> Create Healing Spaces</li>
        </ul>
      </div>

      <!-- Ecosystem Restoration -->
      <div class="p-8 text-center">
        <img src="{% static 'images/ecosystem-restoration.jpg' %}" alt="Ecosystem Restoration"
          class="w-full h-64 object-cover rounded-lg mb-6" />
        <h3 class="text-2xl font-semibold text-secondary mb-4">
          Ecosystem Restoration 🌳
        </h3>
        <ul class="text-darkBrown text-left space-y-2 ml-8">
          <li><i class="fas fa-paw mr-2"></i> Provide Animal Habitats</li>
          <li><i class="fas fa-sun mr-2"></i> Regulate Climate</li>
          <li><i class="fas fa-seedling mr-2"></i> Preserve Biodiversity</li>
        </ul>
      </div>

      <!-- Sustainable Solutions -->
      <div class="p-8 text-center">
        <img src="{% static 'images/sustainable-solutions.jpg' %}" alt="Sustainable Solutions"
          class="w-full h-64 object-cover rounded-lg mb-6" />
        <h3 class="text-2xl font-semibold text-secondary mb-4">
          Sustainable Solutions 🌱
        </h3>
        <ul class="text-darkBrown text-left space-y-2 ml-8">
          <li><i class="fas fa-recycle mr-2"></i> Reduce Carbon Footprint</li>
          <li>
            <i class="fas fa-bread-slice mr-2"></i> Secure Global Food Systems
          </li>
          <li>
            <i class="fas fa-globe-americas mr-2"></i> Restore Environmental
            Balance
          </li>
        </ul>
      </div>
    </div>

  </section>

  <!-- Adaptive Green Solutions -->
  <section class="bg-saffron/10 py-24">
    <div class="container mx-auto text-center mb-12">
      <h2 class="text-3xl md:text-4xl font-bold text-secondary mb-6">
        Custom Green Solutions for Every Space 🌍
      </h2>
      <p class="text-lg text-darkBrown max-w-3xl mx-auto">
        No matter where you are, we have plants that fit your space and
        lifestyle, from urban apartments to rural landscapes.
      </p>
    </div>

    <div class="grid md:grid-cols-3 gap-16">
      <!-- Urban Living -->
      <div class="p-8 text-center">
        <img src="{% static 'images/urban-living.jpg' %}" alt="Urban Living"
          class="w-full h-64 object-cover rounded-lg mb-6" />
        <h3 class="text-2xl font-semibold text-secondary mb-4">
          Urban Living 🌿
        </h3>
        <ul class="text-darkBrown text-left space-y-2 ml-8">
          <li><i class="fas fa-building mr-2"></i> Perfect for Small Spaces</li>
          <li><i class="fas fa-leaf mr-2"></i> Indoor Plants</li>
          <li><i class="fas fa-cogs mr-2"></i> Low Maintenance Options</li>
        </ul>
      </div>

      <!-- Rural Spaces -->
      <div class="p-8 text-center">
        <img src="{% static 'images/rural-farming.jpeg' %}" alt="Rural Spaces"
          class="w-full h-64 object-cover rounded-lg mb-6" />
        <h3 class="text-2xl font-semibold text-secondary mb-4">
          Rural & Agricultural Spaces 🌱
        </h3>
        <ul class="text-darkBrown text-left space-y-2 ml-8">
          <li>
            <i class="fas fa-tractor mr-2"></i> Hardy Varieties for Outdoors
          </li>
          <li>
            <i class="fas fa-globe-americas mr-2"></i> Promote Biodiversity
          </li>
          <li><i class="fas fa-leaf mr-2"></i> Support Sustainable Farming</li>
        </ul>
      </div>

      <!-- Global Accessibility -->
      <div class="p-8 text-center">
        <img src="{% static 'images/global-accessibility.jpeg' %}" alt="Global Accessibility"
          class="w-full h-64 object-cover rounded-lg mb-6" />
        <h3 class="text-2xl font-semibold text-secondary mb-4">
          Global Accessibility 🌏
        </h3>
        <ul class="text-darkBrown text-left space-y-2 ml-8">
          <li><i class="fas fa-shipping-fast mr-2"></i> Worldwide Shipping</li>
          <li><i class="fas fa-users mr-2"></i> Expert Guidance</li>
          <li><i class="fas fa-archive mr-2"></i> Diverse Plant Selection</li>
        </ul>
      </div>
    </div>

  </section>

  <!-- Join the Global Green Family -->
  <section class="bg-tertiary/10 py-24">
    <div class="container mx-auto text-center">
      <h2 class="text-3xl md:text-4xl font-bold text-secondary mb-6">
        Join the Grow Earth Movement 🌍
      </h2>
      <p class="text-lg text-darkBrown mb-8 max-w-2xl mx-auto">
        Let’s work together to create a greener future. Every plant you grow
        strengthens our planet and nurtures well-being.
      </p>
      <div class="flex justify-center space-x-6">
        <a href="{% url 'store:categoryes' %}"
          class="bg-primary text-white px-10 py-5 rounded-full hover:bg-primary/90 transition duration-300 transform hover:scale-105">
          <i class="fas fa-seedling mr-2"></i> Explore Our Collection
        </a>
      </div>
    </div>
  </section>
</div>
{% endblock %}
