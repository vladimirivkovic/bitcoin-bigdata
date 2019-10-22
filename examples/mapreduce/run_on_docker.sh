#!/bin/bash
docker cp . resourcemanager:/bitcoin
docker exec -it nodemanager bash -c "apt update && apt install python -y"
docker exec -it resourcemanager bash -c "chmod +x /bitcoin/compile-and-run.sh && /bitcoin/compile-and-run.sh"