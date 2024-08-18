#!/bin/sh
sudo openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
    -keyout /etc/ssl/private/halfass_it.key \
    -out /etc/ssl/certs/halfass_it.crt \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"
sudo openssl dhparam -out /etc/ssl/certs/dhparam.pem 4096
mkdir -p /etc/nginx/snippets
sudo cp ./router/ssl-params.conf /etc/nginx/snippets/ssl-params.conf
