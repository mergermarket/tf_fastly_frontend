FROM python:3-alpine3.6
COPY requirements.txt .

ENV TERRAFORM_VERSION=0.11.7

ENV TERRAFORM_PROVIDER_FASTLY_VERSION=0.1.4
ENV TERRAFORM_PROVIDER_LOGENTRIES_VERSION=0.1.0_logset_datasource

RUN echo http://dl-cdn.alpinelinux.org/alpine/latest-stable/main >> /etc/apk/repositories
RUN apk update
RUN apk -U add gcc musl-dev libffi-dev openssl-dev docker curl git zip unzip wget

RUN cd /tmp && \
    curl -sSLO https://releases.hashicorp.com/terraform/$TERRAFORM_VERSION/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
        unzip terraform_*_linux_amd64.zip -d /usr/bin && \
    curl -sSLO https://releases.hashicorp.com/terraform-provider-fastly/$TERRAFORM_PROVIDER_FASTLY_VERSION/terraform-provider-fastly_${TERRAFORM_PROVIDER_FASTLY_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-fastly_*_linux_amd64.zip -d /usr/bin && \
    wget -q https://s3-eu-west-1.amazonaws.com/mmg-terraform-providers/terraform-provider-logentries_v${TERRAFORM_PROVIDER_LOGENTRIES_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-logentries_*_linux_amd64.zip -d /usr/bin && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/*


ENV PYTHONDONTWRITEBYTECODE donot

RUN pip install --no-cache-dir -r requirements.txt
ADD infra /infra
