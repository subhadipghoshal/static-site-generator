# Makefile

# Python project config
PYTHON := uv run python
TEST_DIR := tests
SRC_DIR := src

# Default goal
.DEFAULT_GOAL := help

help:
	@echo "Common commands:"
	@echo "  make install       Install dependencies using uv"
	@echo "  make bootstrap     Set up the development environment"
	@echo "  make test          Run all unit tests"
	@echo "  make test-file f=tests/test_example.py"
	@echo "  make test-method m=tests.test_example.TestFoo.test_bar"
	@echo "  make coverage      Run tests with coverage"
	@echo "  make clean         Remove __pycache__ and artifacts"

install:
	uv sync

bootstrap: install test
	@echo "Development environment is set up."

test:
	$(PYTHON) -m unittest discover -s $(TEST_DIR) -v

test-file:
	@if [ -z "$(f)" ]; then \
		echo "Error: missing param f=<path-to-test>"; \
		exit 1; \
	fi
	$(PYTHON) -m unittest $(f)

test-method:
	@if [ -z "$(m)" ]; then \
		echo "Error: missing param m=<module.class.method>"; \
		exit 1; \
	fi
	$(PYTHON) -m unittest $(m)

coverage:
	uv run coverage run -m unittest discover -s $(TEST_DIR)
	uv run coverage report -m

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -f .coverage

