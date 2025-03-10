# Makefile for Grow Earth Online Plant Store

# Project Directories
SRC_DIR := src
MANAGE := $(SRC_DIR)/manage.py

# Python and Virtual Environment
PYTHON := uv run python
VENV := .uv

# Colors
GREEN := \033[0;32m
NC := \033[0m

# Default target
.PHONY: help
help:
	@echo "$(GREEN)Grow Earth Project Management$(NC)"
	@echo "Available commands:"
	@echo "  setup       - Create virtual environment and install dependencies"
	@echo "  run         - Run Django development server"
	@echo "  migrate     - Create and apply database migrations"
	@echo "  test        - Run project tests"
	@echo "  lint        - Run code linting"
	@echo "  clean       - Remove cached files"
	@echo "  full_clean  - Remove cached files and clean project"
	@echo "  superuser   - Create superuser in django website to manage database"

# Setup project environment
.PHONY: setup
setup:
	@echo "$(GREEN)Setting up project environment...$(NC)"
	uv venv
	uv pip install -r requirements.txt
	uv pip install -e .



.PHONY: tailwind tailwind-install tailwind-start dev

# Tailwind CSS Build
tailwind:
	@echo "$(GREEN)Building Tailwind CSS...$(NC)"
	cd $(SRC_DIR) && npx tailwindcss -i ./static/src/input.css -o ./static/css/tailwind.css

# Install Tailwind
tailwind-build:
	@echo "$(GREEN)Installing Tailwind CSS...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py tailwind build

# Start Tailwind Compilation
tailwind-watch:
	@echo "$(GREEN)Starting Tailwind CSS Compilation...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py tailwind watch

# Development Server
dev:
	@echo "$(GREEN)Starting Development Server...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py tailwind runserver 0.0.0.0:8000

# Create Superuser
.PHONY: superuser
superuser:
	@echo "$(GREEN)Creating Django Superuser...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py createsuperuser


# Database Migrations
.PHONY: migrate
migrate:
	@echo "$(GREEN)Creating database migrations...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py makemigrations
	cd $(SRC_DIR) && $(PYTHON) manage.py migrate


.PHONY: populate_store
populate_store:
	@echo "$(GREEN)Populate store...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py collectstatic --noinput
	cd $(SRC_DIR) && $(PYTHON) manage.py populate_store

 
# Run Tests
.PHONY: test
test:
	@echo "$(GREEN)Running project tests...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) -m pytest

# Code Linting
.PHONY: lint
lint:
	@echo "$(GREEN)Running code linters...$(NC)"
	ruff check $(SRC_DIR)
	black --check $(SRC_DIR)

# Clean Project
.PHONY: clean
clean:
	@echo "$(GREEN)Cleaning project...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +


# Clean Full Project with database and database used images
.PHONY: full_clean
clean:
	@echo "$(GREEN)Cleaning project...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	rm -rf src/static/css/tailwind.css
	rm -rf src/db.sqlite3
	rm -rf src/media/category_images/*
	rm -rf src/media/plant_images/*