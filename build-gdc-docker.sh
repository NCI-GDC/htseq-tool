#!/bin/bash
# Only relevant for building the imagine within the GDC system

docker_build () {
    command docker build \
        --build-arg http_proxy=$http_proxy \
        --build-arg https_proxy=$https_proxy \
        --force-rm --rm \
        "$@"
}

quay="quay.io/ncigdc/htseq-tool"
version=$(git log --first-parent --max-count=1 --format=format:%H)
imagetag="${quay}:${version}"

echo "Building tag: $imagetag"
docker_build -t $imagetag .
