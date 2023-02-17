#!/bin/bash
docker stop g4bls_worker_1
VOLUMEDIRECTORY=./g4bls_volume
if [ ! -d "$VOLUMEDIRECTORY" ]; then
    mkdir -p "$VOLUMEDIRECTORY"
fi



docker-compose --compatibility -p g4bls -f docker-compose.yml up -d --build $@


docker logs -f --tail 20 g4bls_worker_1
