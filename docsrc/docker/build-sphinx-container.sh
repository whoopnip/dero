#!/bin/bash

#IMAGE=$(docker images python3-sphinx | tail -n +2);
#
#if [ "$IMAGE" ]; then
#    echo "Found python3-sphinx image";
#
#    exit 0;
#fi

REPO_DIR=$(realpath ../)
SPHINX_DIR="$REPO_DIR/docsrc"
DOCKER_DIR="$SPHINX_DIR/docker"

cp "$REPO_DIR/requirements.txt" "$DOCKER_DIR"

docker build "$DOCKER_DIR" -t python3-sphinx;
