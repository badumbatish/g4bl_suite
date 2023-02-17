#!/bin/bash

set -e

chmod 775 ./compile-all.sh

export GOOS=linux
export GOARCH=amd64
./compile-all.sh

unset GOOS
unset GOARCH
