FROM python:3-alpine3.7
COPY requirements.txt .
COPY pycharm-debug-py3k.egg .

ENV TERRAFORM_VERSION=0.11.7

ENV TERRAFORM_PROVIDER_FASTLY_VERSION=0.1.4

RUN echo http://dl-cdn.alpinelinux.org/alpine/latest-stable/main >> /etc/apk/repositories
RUN apk update
RUN apk -U add gcc musl-dev libffi-dev openssl-dev docker curl git zip unzip wget

ENV TERRAFORM_PLUGIN_DIR=/root/.terraform.d/plugins/

RUN mkdir -p "${TERRAFORM_PLUGIN_DIR}" && cd /tmp && \
    curl -sSLO "https://releases.hashicorp.com/terraform/$TERRAFORM_VERSION/terraform_${TERRAFORM_VERSION}_linux_amd64.zip" && \
        unzip "terraform_${TERRAFORM_VERSION}_linux_amd64.zip" -d /usr/bin && \
    curl -sSLO "https://releases.hashicorp.com/terraform-provider-fastly/$TERRAFORM_PROVIDER_FASTLY_VERSION/terraform-provider-fastly_${TERRAFORM_PROVIDER_FASTLY_VERSION}_linux_amd64.zip" && \
        unzip "terraform-provider-fastly_${TERRAFORM_PROVIDER_FASTLY_VERSION}_linux_amd64.zip" -d "${TERRAFORM_PLUGIN_DIR}" && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/*


ENV PYTHONDONTWRITEBYTECODE donot

RUN pip install --no-cache-dir -r requirements.txt
ADD infra /infra
