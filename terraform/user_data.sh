#!/bin/bash
apt-get update -y
apt-get install -y docker.io docker-compose git curl
systemctl start docker
systemctl enable docker
usermod -aG docker ubuntu

git clone https://github.com/yogyatha12345/smrithi.git /home/ubuntu/smrithi || true
cd /home/ubuntu/smrithi
docker-compose up -d --build
