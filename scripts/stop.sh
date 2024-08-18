#!/bin/sh

sudo systemctl stop nginx
sudo kill -9 $(sudo fuser 5000/tcp 5001/tcp 5002/tcp 5003/tcp 5004/tcp) >/dev/null 2>&1
sudo kill -9 $(sudo fuser 6000/tcp 6001/tcp 6002/tcp) >/dev/null 2>&1
sudo kill -9 $(sudo fuser 7000/tcp 7001/tcp 7002/tcp) >/dev/null 2>&1
