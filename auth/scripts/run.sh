#!/bin/sh
go build .
sudo ./auth -start &
tail -f ./brewTV.log
