# Makefile for Grow Earth Online Plant Store

# Project Directories
SRC_DIR := src
MANAGE := $(SRC_DIR)/manage.py

# Python and Virtual Environment
PYTHON := uv run python
VENV := .uv

# Colors for output
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
	@echo "  superuser   - Create superuser in Django website to manage database"
	@echo "  tailwind    - Build Tailwind CSS"
	@echo "  tailwind-watch - Start Tailwind CSS compilation in watch mode"

# Setup project environment
.PHONY: setup
setup:
	@echo "$(GREEN)Setting up project environment...$(NC)"
	uv venv
	uv pip install -r requirements.txt
	uv pip install -e .

# Tailwind CSS Build
.PHONY: tailwind tailwind-install tailwind-watch

tailwind:
	@echo "$(GREEN)Building Tailwind CSS...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py tailwind build

# Start Tailwind Compilation in watch mode
tailwind-watch:
	@echo "$(GREEN)Starting Tailwind CSS Compilation...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py tailwind watch

# Development Server
.PHONY: dev run

dev:
	@echo "$(GREEN)Starting Development Server...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py tailwind runserver 0.0.0.0:8000

run:
	@echo "$(GREEN)Starting Server...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py runserver 0.0.0.0:8000

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

# Populate Store (collect static files and other tasks)
.PHONY: populate_store
populate_store:
	@echo "$(GREEN)Populating store...$(NC)"
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

# Clean Project (remove cached files)
.PHONY: clean
clean:
	@echo "$(GREEN)Cleaning project...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +

# Full Clean Project (remove all cached files and reset database)
.PHONY: full_clean
full_clean: clean
	@echo "$(GREEN)Performing full clean of the project...$(NC)"
	rm -rf src/static/css/tailwind.css      # Remove generated Tailwind CSS file
	rm -rf src/db.sqlite3                   # Remove SQLite database file
	rm -rf src/media/category_images/*       # Remove category images from media folder
	rm -rf src/media/plant_images/*          # Remove plant images from media folder

