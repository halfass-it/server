#!/bin/sh

docker pull ollama/ollama
docker build -t llmpeg -f ci/llmpeg.Dockerfile .
