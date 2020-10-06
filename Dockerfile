FROM python:3.8-slim-buster

RUN pip install \
    cookiecutter==1.6.0 \
    colorama==0.4.3 \
    PyYAML==5.3.1    

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git curl gnupg

COPY ./heroku-install-debian.sh /usr/local/bin
RUN /usr/local/bin/heroku-install-debian.sh

RUN useradd -m sid
USER sid
