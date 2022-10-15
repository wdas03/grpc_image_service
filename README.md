This repo contains four executables (setup, build, server, and client), each which, respectively, installs packages and dependencies in the code environment, builds necessary grpc protobuf files, runs the server service, and runs the client service. I additionally dockerized the server and client services into images which operate using Docker's network host capabilities, briefly documented below.

# Usage

Should be run on a fresh MacOS install. Docker Desktop should be installed from online (https://docs.docker.com/desktop/install/mac-install/).

## Files
- _server.py_: Runs the image service server
- _client.py_: Runs the client request
- _config.py_: Rotation enum + OpenCV constants
- _image_utils.py_: Image handling functions
- _test_client_server.py_: Unit tests for image handling/server processing
- __server_: 
    - _Dockerfile_: Dockerfile for server image
    - _run_server.sh_: Entrypoint script that runs server.py in container given command-line args
- __client_: 
    - _Dockerfile_: Dockerfile for client image
    - _run_client.sh_: Entrypoint script that runs client.py in container given command-line args
- _setup_: Sets up conda environment (grpc_env) and packages/dependencies
- _build_: Creates grpc protobuf files
- _server_: Runs grpc server in conda env (wraps server.py)
- _client_: Runs grpc client in conda env (wraps client.py)
- _images_: Test images

## Setup Script
From project home directory, run:
> `chmod +x setup build client server`
> 
> `./setup`

This creates a conda environment called grpc_env, where the _./server_ and _./client_ scripts are run in, and all python files should be run in.

## Build Script
After _./setup_, run ./build:
> `./build`

This generates grpc files from the protobuf spec.

## Setup + Build

> `chmod +x setup build client server`
>
> `./setup`
>
> `./build`

## Server Script
To run the server service on a local machine, run ./server:

> `./server --port 50510 --host localhost`

Alternatively, activate grpc_env and run server.py:

> `conda activate grpc_env`
>
> `python server.py --port 50510 --host localhost`

`source ~/.bash_profile` may need to be run before activating the conda environment.

## Client Script
Similarly, to run client script on a local machine:

> `./client --port 50510 --host localhost --input images/roger.jpeg --output images/roger_trans.jpeg --rotate NINETY_DEG --mean`

# Running Dockerized Containers
The _server and _client folders contain Dockerfiles for creating separate images for the server and client services. Docker should be installed and running on the local machine. 

## Server Interface

### Build Server Image
To build the grpc_server image on your local machine, run from the project home directory, outside the _server and _client folders:

> `docker build -f _server/Dockerfile . -t grpc_server`

### Build Client Image
To build grpc_client image, run from the project home directory:

> `docker build -f _client/Dockerfile . -t grpc_client`

### Run Server Container
To start running the server on the network host, on localhost:50510 for example, run:

> `docker run -it --net host grpc_server "--port 50510 --host localhost"`

The port and host parameters should be specified at the end with double-dashed flags: "--port 50510 --host localhost".


Alternatively, if you only want to run the Docker server in a container and connect via a Python script on the local machine (if you want to view the transformed image on your local machine, as opposed to a Docker container), you can expose and publish ports to your local machine from the server container by running in one terminal:

> `docker run -it --expose=50510 -p 50510:50510 grpc_server "--port 50510 --host localhost"`

On another terminal, you can then run the client script:

> `./client --port 50510 --host localhost --input images/roger.jpeg --output images/roger_trans.jpeg --rotate NINETY_DEG --mean`

## Client Interface

### Run Client Container
To run the client script in a Docker container using the network host, run:

> `docker run -it --net host grpc_client "--port 50510 --host localhost --input images/roger.jpeg --output images/roger_trans.jpeg --rotate NINETY_DEG --mean"`

The last argument in quotations are arguments you would input into the _client_ script.

One way to view the transformed image stored on the container is by copying the file from the container, using the containter ID, (from the client_interface folder) to your local machine:

> `docker cp container_id:/client_interface/images/roger_trans.jpeg roger_trans_docker.jpeg`

## Server + Client Docker Containers

> `docker build -f _server/Dockerfile . -t grpc_server`
>
> `docker build -f _client/Dockerfile . -t grpc_client`

### Running on Containers
On one terminal:
> `docker run -it --net host grpc_server "--port 50510 --host localhost"`

On another terminal:
> `docker run -it --net host grpc_client "--port 50510 --host localhost --input images/roger.jpeg --output images/roger_trans.jpeg --rotate NINETY_DEG --mean"`

Copy output image to local machine:
> `docker cp container_id:/client_interface/images/roger_trans.jpeg roger_trans_docker.jpeg`

### Dockerized Server + Local Python Script
On one terminal
> `docker run -it --expose=50510 -p 50510:50510 grpc_server "--port 50510 --host localhost"`

On another terminal, you can then run the client script:

> `./client --port 50510 --host localhost --input images/roger.jpeg --output images/roger_trans.jpeg --rotate NINETY_DEG --mean`

## Unit Tests
On one terminal, server should be running on _localhost:8080_:
> `./server --port 8080 --host localhost`

On another terminal, in _grpc_env_ env:
> `python test_client_server.py`
