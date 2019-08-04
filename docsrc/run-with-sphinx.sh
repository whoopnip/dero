#!/bin/bash

bash ./docker/build-sphinx-container.sh

if [ $? -ne 0 ]; then
    >&2 echo "Error building python3-sphinx container";

    exit 1;
fi

docker run --rm -it -v $(realpath ..):/dero python3-sphinx "$@"