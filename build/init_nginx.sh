#!/bin/sh

DOMAIN="$1"
CONFIG_PATH="/etc/nginx/sites-available/server.nginx"

# Check if DOMAIN argument is provided
if [ -z "$DOMAIN" ]; then
  echo "Usage: $0 <domain>"
  exit 1
fi

# Copy the Nginx configuration template to the sites-available directory
sudo cp ./router.nginx $CONFIG_PATH

# Replace 'your_domain.com' with the provided domain in the configuration file
sudo sed -i "s/your_domain.com/$DOMAIN/g" $CONFIG_PATH

# Create a symbolic link to enable the site
sudo ln -s $CONFIG_PATH /etc/nginx/sites-enabled/

# Obtain SSL/TLS certificates using Certbot
sudo certbot --nginx -d $DOMAIN

# Start and enable Nginx service
sudo systemctl start nginx
sudo systemctl enable nginx

echo "Nginx server setup complete for domain: $DOMAIN"

