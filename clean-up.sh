#/bin/sh

docker rm -f $(docker ps -aq)
docker volume rm -f $(docker volume ls -q)
# docker rmi -f bitcoin-bigdata_consumer bitcoin-bigdata_producer
