FROM python:3.10
MAINTAINER rmpeter0474

LABEL version='1.0'
LABEL description='python3.10 with django '

WORKDIR /
COPY requirements.txt ./
RUN mkdir /tmp/log
RUN mkdir /static

RUN python -m venv venv \
 && . venv/bin/activate \
 && pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt
