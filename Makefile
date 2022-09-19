.PHONY: all
all: test

.PHONY: test
test:
	python -m pytest
