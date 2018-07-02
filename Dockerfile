FROM debian:latest
ENV DEBIAN_FRONTEND noninteractive

WORKDIR /work


RUN apt-get update; \
    apt-get install -y python-setuptools python-dev python-gdal;\
    easy_install pip; pip install wheel;

COPY requirements.txt /work/requirements.txt
COPY requirements-dev.txt /work/requirements-dev.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
WORKDIR /work
CMD /bin/bash
