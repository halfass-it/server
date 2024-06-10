FROM python:3.11

# Globally install poetry and upgrade pip things
# (NOTE: the poetry project often releases new versions over weekends, so
#        if your have auto-building services and poetry releases a new incompatible
#        version, your stuff will just break randomly on Saturday nights; so you _could_
#        pin your specific poetry version here, but also fix-as-it-breaks is valid too)

# Install system dependencies
# espeak and ffmpeg
RUN apt-get update && apt-get install -y espeak ffmpeg
# vlc
RUN apt-get update && apt-get install -y \
    vlc \
    libvlc-dev
    # && apt-get clean \
    # && rm -rf /var/lib/apt/lists/*
# selenium
RUN apt-get install -yq \
    chromium \
    chromium-driver \
    fonts-ipafont-gothic \
    fonts-wqy-zenhei \
    fonts-thai-tlwg \
    fonts-kacst \
    fonts-freefont-ttf \
    fonts-liberation \
    fonts-arphic-uming
# alsa
RUN apt-get install -yq \
    alsa-utils
# sounddevice
RUN apt-get install -yq \
    libportaudio2 \
    libportaudiocpp0 \
    libsndfile1
# soundfile
RUN apt-get install -yq \
    libsndfile1
# ollama
RUN apt-get install -yq \
    libsm6 \
    libxext6 \
    libxrender-dev
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install poetry
RUN pip install pip poetry setuptools wheel -U --no-cache-dir

# Set the working directory
WORKDIR /app

# Copy the poetry files
COPY pyproject.toml poetry.lock /app/

# Install project the dependencies
# Run the virtual env creator and dependency installer
# (NOTE: some python packages like mysqlclient require more system binary packages
#        to be installed, so you'd need to apt-get other packages as required before
#        your poetry install if needed)
RUN poetry install --no-dev --no-interaction --no-ansi --no-root --no-cache 

# Copy project files
COPY ./llmpeg /app/llmpeg 

# Now install the project package itself
# NOTE: Yes, we run `poetry install` TWICE due to the docker
#       caching logic because we don't want to reinstall dependencies
#       on every code update. This means the dependencies are cached
#       in the _first_ `poetry install` layer, while _this_ `poetry install`
#       layer just handles a final "script cleanup" install due to path issues.
RUN poetry install --no-dev --no-interaction --no-ansi --no-root --no-cache 

# Set environment variables

# Run command (as defined in `pyproject.toml` poetry scripts section)
CMD ollama pull "gemma:2b"; poetry run main "gemma:2b" "punkt" "small" "tiny" run
