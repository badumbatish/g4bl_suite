#!/bin/bash
set -e

echo "Compiling started -" `date`
unset GOPATH

export GOCACHE=`pwd`/.buildenv-cache
mkdir -p "$GOCACHE"/.buildenv-cache

pushd .
cd ./src/golang

go build -o ../../docker/worker/golang

popd

echo "Compile finished -" `date`