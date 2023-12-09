#!/usr/bin/env bash
# This script sets up web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get -y update
    sudo apt-get -y install nginx
fi
hostname=$(hostname)

# Remove existing web_static directories with timestamps
sudo rm -rf /data/web_static/releases/web_static_*

# Create necessary folders if they don't exist
sudo rm -rf /data/web_static/releases/test/
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
sudo touch /data/web_static/releases/test/index.html

# Create a fake HTML file for testing
echo -e "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create or recreate symbolic link
sudo rm -f /data/web_static/current
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ folder to the ubuntu user and group recursively
sudo chown -R ubuntu:ubuntu /data/
placement="server_name $hostname;\n\tlocation \/hbnb_static\/ {\n\t\talias \/data\/web_static\/current\/;\n\t}"
sudo sed -i "s#server_name $hostname;#$placement#" /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
