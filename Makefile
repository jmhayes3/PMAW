.PHONY:	all clean test lint
all:	clean test lint
clean:
	find . -name '__pycache__' -exec rm -rf {} +
test:
	pytest tests/ -v
lint:
	flake8 --exit-zero pmaw
