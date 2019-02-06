FROM python:3-alpine3.8
COPY requirements.txt .

ENV TERRAFORM_VERSION=0.11.11

RUN echo http://dl-cdn.alpinelinux.org/alpine/latest-stable/main >> /etc/apk/repositories
RUN apk update
RUN apk -U add gcc musl-dev libffi-dev openssl-dev docker curl git zip unzip wget

RUN cd /tmp && \
    curl -sSLO "https://releases.hashicorp.com/terraform/$TERRAFORM_VERSION/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" && \
        unzip "terraform_${TERRAFORM_VERSION}_linux_amd64.zip" -d /usr/bin && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/*

ENV PYTHONDONTWRITEBYTECODE donot

RUN pip install --no-cache-dir -r requirements.txt
ADD infra /infra
