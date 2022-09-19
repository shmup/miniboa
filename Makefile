.PHONY: all
all: test

.PHONY: pypi
pypi:
	python3 -m build
	python3 -m twine upload --repository miniboa dist/*

.PHONY: test
test:
	python -m pytest
