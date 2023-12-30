#! /bin/bash
dnf update -y
dnf install docker -y
systemctl start docker
systemctl enable docker
usermod -a -G docker ec2-user
newgrp docker
dnf install git -y
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
cd /home/ec2-user/
mkdir project && cd project
FOLDER=https://raw.githubusercontent.com/turangozukara/Dockerization-Bookstore-Api-On-Python-Flask-MySQL/main
wget $FOLDER/Dockerfile
wget $FOLDER/bookstore-api.py
wget $FOLDER/docker-compose.yml
wget $FOLDER/requirements.txt
docker-compose up -d