# Format source code automatically
style:
	black --line-length 119 --target-version py37 src/charcut
	isort src/charcut

# Control quality
quality:
	black --check --line-length 119 --target-version py37 src/charcut
	isort --check-only src/charcut
	flake8 src/charcut --exclude __pycache__,__init__.py

# Run tests
test:
	pytest tests
