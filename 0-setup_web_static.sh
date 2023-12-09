sh script to set up web servers for deployment of web_static

# Install Nginx if not already installed
apt-get -y update
apt-get -y install nginx

# Create necessary folders
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file for testing
echo -e '<html>\n\t<head>\n\t</head>\n\t<body>\n\t\tHolberton School\n\t</body>\n</html>' > /data/web_static/releases/test/index.html

# Create symbolic link
if [ -L /data/web_static/current ]; then
    rm /data/web_static/current
fi
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config="location /hbnb_static {\n\talias /data/web_static/current/;\n}\n"
sed -i "s#server_name _;#$config#" /etc/nginx/sites-available/default

# Restart Nginx
service nginx restart

exit 0
