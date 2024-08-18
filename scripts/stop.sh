#!/bin/sh

sudo systemctl stop nginx
sudo kill -9 $(sudo fuser 5001/tcp 5002/tcp 5003/tcp 5004/tcp) >/dev/null 2>&1
sudo kill -9 $(sudo fuser 6001/tcp 6002/tcp) >/dev/null 2>&1
sudo kill -9 $(sudo fuser 7001/tcp 7002/tcp) >/dev/null 2>&1
