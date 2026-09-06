# Copyright 2026 Luke Steuber. MIT License.
PEBBLE ?= pebble
PYTHON ?= python3
HOST_CC ?= clang
.PHONY: build test assets package
build: test
	$(PEBBLE) build --sdk 4.33.1
test:
	mkdir -p build
	$(HOST_CC) -DORCHID_HOST -std=c11 -fsanitize=address,undefined -Wall -Wextra -Werror test/time.c src/c/orchid.c -lm -o build/time-test
	./build/time-test
	$(PYTHON) test/geometry.py
assets:
	mkdir -p build
	$(PYTHON) tools/assets.py
package:
	$(PYTHON) test/package.py
