.PHONY: test run build-docker run-docker

# Variables
IMAGE_NAME := geotif
CONTAINER_NAME := geotif-container
LOCAL_DATA_DIR := /home/ismaello/iceye/data-engineer-assignment/data
CONTAINER_DATA_DIR := /app/data
INPUT_FILE := data/input/ICEYE_X4_GRD_SM_9281_20190903T144955.tif
OUTPUT_FORMAT := 0-1
MAX_SIZE := 256 256
OUTPUT_FILE := data/output/output_file.png

# Define the default target
all: test run build-docker

# Target for running tests
test:
	pytest

# Target for running the application
run:
	python3 geotif.py $(INPUT_FILE) $(OUTPUT_FORMAT) $(MAX_SIZE) $(OUTPUT_FILE)

# Target for building the Docker image
build-docker:
	docker build -t $(IMAGE_NAME) .

# Example target for running Docker container
run-docker:
	docker run --name $(CONTAINER_NAME) -v $(LOCAL_DATA_DIR):$(CONTAINER_DATA_DIR) $(IMAGE_NAME) $(INPUT_FILE) $(OUTPUT_FORMAT) $(MAX_SIZE) $(OUTPUT_FILE)

# Target for running tests and building Docker image
test-build-docker: test build-docker