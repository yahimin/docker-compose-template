#!/bin/bash
set -x
yum update -y
yum install docker -y

systemctl start docker
systemctl enable docker


echo "############### Chechking Docker service status ################"
systemctl is-enabled docker


usermod -a -G docker ec2-user
chmod 666 /var/run/docker.sock

DOCKER_CONFIG="$HOME/.docker"
echo "$DOCKER_CONFIG"

mkdir -p $DOCKER_CONFIG/cli-plugins

curl -SL https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose

chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
