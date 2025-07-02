#!/bin/bash
# install_nginx.sh

sudo apt update -y
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
echo "<h1>Hello from Terraform deployed Nginx!</h1>" | sudo tee /var/www/html/index.nginx-debian.html