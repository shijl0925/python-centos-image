#!/bin/bash

docker create -t -i --name test-container ${DOCKERHUB_USERNAME}/centos-${CENTOS_VERSION}-python:${PYTHON_VERSION}
docker start test-container
docker exec -i test-container python3 < src/${PYTHON_VERSION%.*}/test_image.py
docker exec -i test-container python3 -m test -v
