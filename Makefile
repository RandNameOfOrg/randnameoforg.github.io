.ONESHELL:
.PHONY: build package_install

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

define done
	clear
	@echo -e "\e[32mDone\e[0m"
endef

package_install:
	python3 -m pip install --upgrade pip
	pip3 install -r $(PROJECT_DIR)/requierments.txt
	$(call done)

build:
	cd $(PROJECT_DIR) && if [ ! -d "build_output" ]; then mkdir build_output; fi
	python3 $(PROJECT_DIR)/build.py --output="build_output"
	$(call done)