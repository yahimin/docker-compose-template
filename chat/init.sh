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

DOCKER_COMPOSE_VERSION="1.29.2"
curl -SL "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose



