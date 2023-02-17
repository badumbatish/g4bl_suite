#!/bin/bash
docker stop g4bls_manager_1

VOLUME_DIR=./g4bls_volume

if [ ! -d "$VOLUME_DIR" ]; then
  mkdir -p "$VOLUME_DIR"
fi

if ! ./build.sh; then
  echo "Build failed"
  exit 1
fi

docker-compose --compatibility -p g4bls -f docker-compose.yml up -d --build $@

docker logs -f --tail 20 g4bls_worker_1
