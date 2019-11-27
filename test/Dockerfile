FROM python:3-alpine3.8

ENV TERRAFORM_VERSION=0.11.11
ENV PYTHONDONTWRITEBYTECODE donot

RUN echo http://dl-cdn.alpinelinux.org/alpine/latest-stable/main >> /etc/apk/repositories && \
    apk update && \
    apk add curl

RUN cd /tmp && \
    curl -sSLO "https://releases.hashicorp.com/terraform/$TERRAFORM_VERSION/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" && \
        unzip "terraform_${TERRAFORM_VERSION}_linux_amd64.zip" -d /usr/bin && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ADD infra /infra
