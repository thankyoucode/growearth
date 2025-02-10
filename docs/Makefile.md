## Makefile for Grow Earth Django Project

```makefile
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
	@echo "  clean       - Remove cached files and clean project"

# Setup project environment
.PHONY: setup
setup:
	@echo "$(GREEN)Setting up project environment...$(NC)"
	uv venv
	uv pip install -r requirements.txt
	uv pip install -e .

# Run development server
.PHONY: run
run:
	@echo "$(GREEN)Starting Django development server...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py runserver

# Database Migrations
.PHONY: migrate
migrate:
	@echo "$(GREEN)Creating database migrations...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py makemigrations
	cd $(SRC_DIR) && $(PYTHON) manage.py migrate

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

# Create Superuser
.PHONY: superuser
superuser:
	@echo "$(GREEN)Creating Django Superuser...$(NC)"
	cd $(SRC_DIR) && $(PYTHON) manage.py createsuperuser

# Tailwind CSS Build
.PHONY: tailwind
tailwind:
	@echo "$(GREEN)Building Tailwind CSS...$(NC)"
	cd $(SRC_DIR) && npx tailwindcss -i ./static/src/input.css -o ./static/css/tailwind.css
```

## Makefile Setup and Usage

### Prerequisites

- UV (Universal Virtualenv)
- Python 3.10+
- Make utility

### Installation Steps

1. Ensure Make is installed on your system
2. Install UV: `pip install uv`
3. Place Makefile in project root

### Basic Usage

```bash
# Show available commands
make help

# Setup project environment
make setup

# Run development server
make run

# Create database migrations
make migrate

# Run tests
make test

# Clean project
make clean
```

## Best Practices

- Use descriptive target names
- Add color for better readability
- Provide help documentation
- Support common development workflows
- Keep commands simple and focused

This Makefile provides a comprehensive set of commands to streamline your Django project development process.
