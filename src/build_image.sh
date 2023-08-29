#!/bin/bash

# Build the corresponding image
docker build --no-cache . \
  --file ./src/Dockerfile \
  --tag ${DOCKERHUB_USERNAME}/centos-${CENTOS_VERSION}-python:${PYTHON_VERSION} \
  --build-arg PYTHON_VERSION=${PYTHON_VERSION} \
  --build-arg CENTOS_VERSION=${CENTOS_VERSION} \
  --build-arg QUICK_BUILD="${QUICK_BUILD}"
