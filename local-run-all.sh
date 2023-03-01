#!/bin/bash
docker stop g4bls_manager_1

VOLUME_DIR=./g4bls_volume

if [ ! -d "$VOLUME_DIR" ]; then
  mkdir -p "$VOLUME_DIR"
fi
netw="external-example"
a=$(docker network ls | awk -v netw=$netw '$2==netw {print $2}')
if [[ $a == external-example ]];then
  echo "External network is detected"
else
  echo "External network not detected, creating network"
  docker network create external-example
fi
#docker network create external-example
docker-compose --compatibility -p g4bls -f docker-compose.yml up -d --build $@

#docker logs -f --tail 20 g4bls_worker_1
