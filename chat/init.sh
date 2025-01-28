# EC2 Launch Template shell scrpit

#!/bin/bash
### 스크립트 로그 보기 위한 명령어
set -x
yum update -y

## docker
amzon-linux-extras install docker -y
docker --version

### docker 서비스 시작
service docker start

### docker 부팅시 자동으로 시작 
systemctl enable docker


echo "############### Chechking Docker service status ################"
### docker 서비스 상태 확인 
service docker status 
### docker 부팅시 자동으로 시작되는지 상태확인
systemctl is-enabled docker

### ec2-user를 docker그룹에 추가
### => docker 명령어 사용할때 sudo 입력안해도 되게 설정
usermod -a -G docker ec2-user

### 도커 데몬과 클라이언트와 통신하기 위한 socket파일 권한 설정 (read + write)

- ssh로 ec2-user 그룹에 권한을 설정해줘야 하기에 other 그룹도 6으로 설정해준다.
chmod 666 /var/run/docker.sock

## docker-compose install
curl -SL https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose

docker-compose --version

chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
