# Geotif

A application to convert geotif GRD images to png.

## Getting Started

The project doesn't have images for testing. I use the images for the task. Left the images in the directory data/input.


### Prerequisites

* Python 3.10
* virtualenv
* pytest
* pip
* Pillow
* rasterio


## Build docker image
To build the imagen, you need to run the following command:

```bash
docker build -t geotif .
```

The Dockerfile only will copy geotif.py, requirements.txt and src directory.

## Run docker image
To run the image, you need to run the following command:

```bash
docker run --name geotif-container -v /home/ismaello/iceye/data-engineer-assignment/data:/app/data geotif data/input/ICEYE_X4_GRD_SM_9281_20190903T144955.tif 0-1 256 256 data/output/output_file.png
```
Important: The entrypoint is python3 geotif.py. So, you need to pass the params after the name of the image.
If you want to run a interactive shell, you need to run the docker with the option --entrypoint /bin/bash


# Using Makefile
This project has a Makefile to run the application and the tests. 

To run the tests:

```bash
make test
```

To run the application:
```bash
make run 

```

Test and build docker image:
```bash
make test-build-docker
```

Run docker image:
```bash
make run-docker
```
Build docker image:
```bash
make build-docker
```

Setup your Makefile: 

There are variables on Makefile to setup your environment: 
```bash	
# Variables
IMAGE_NAME := geotif
CONTAINER_NAME := geotif-container
LOCAL_DATA_DIR := /home/ismaello/iceye/data-engineer-assignment/data
CONTAINER_DATA_DIR := /app/data
INPUT_FILE := data/input/ICEYE_X4_GRD_SM_9281_20190903T144955.tif
OUTPUT_FORMAT := 0-1
MAX_SIZE := 256 256
OUTPUT_FILE := data/output/output_file.png
```

### Installing
Create your virtualenv

```bash
virtualenv -p python3 venv
```

Activate your virtualenv
```bash
source venv/bin/activate
```

Install the requirements

```bash
pip install -r requirements.txt
```


## Running the application

The params of the application are:
* input_file: The path of the input file.
* normalization_format: 0-1,-1-1,0-255
* max_size: The max size of the image.(256 256)
* output_file: The path of the output file.

To run the application, you need to run the following command:

```bash
 python3 geotif.py data/input/ICEYE_X4_GRD_SM_9281_20190903T144955.tif 0-1 256 256 data/output/salida.png
```


## Author
Ismael Sanchez Casado
isanchezcasado@gmail.com

## Acknowledgments
* ChatGPT to help me with Sigma0 normalization
* Copilot to accelerate my code