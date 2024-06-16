#!/bin/sh

sudo systemctl stop nginx
sudo kill -9 $(sudo fuser 1337/tcp 1338/tcp 1339/tcp 1340/tcp) >/dev/null 2>&1
