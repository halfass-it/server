#!/bin/sh

# Remove existing containers if they exist
docker rm -f ollama || true
docker rm -f llmpeg || true

docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama
docker run --gpus=all --network host --name llmpeg llmpeg

