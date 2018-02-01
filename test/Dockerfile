FROM python:3-alpine3.6
COPY requirements.txt .

ENV TERRAFORM_VERSION=0.11.1

ENV TERRAFORM_PROVIDER_AWS_VERSION=1.6.0
ENV TERRAFORM_PROVIDER_FASTLY_VERSION=0.1.3
ENV TERRAFORM_PROVIDER_LOGENTRIES_VERSION=0.1.0_logset_datasource
ENV TERRAFORM_PROVIDER_NULL_VERSION=1.0.0
ENV TERRAFORM_PROVIDER_TEMPLATE_VERSION=1.0.0
ENV TERRAFORM_PROVIDER_ACME_VERSION=0.3.0
ENV TERRAFORM_PROVIDER_EXTERNAL_VERSION=1.0.0
ENV TERRAFORM_PROVIDER_TLS_VERSION=1.0.1
ENV TERRAFORM_PROVIDER_DATADOG_VERSION=1.0.3

RUN echo http://dl-cdn.alpinelinux.org/alpine/latest-stable/main >> /etc/apk/repositories
RUN apk update
RUN apk -U add gcc musl-dev libffi-dev openssl-dev docker curl git zip unzip wget

RUN cd /tmp && \
    curl -sSLO https://releases.hashicorp.com/terraform/$TERRAFORM_VERSION/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
        unzip terraform_*_linux_amd64.zip -d /usr/bin && \
    curl -sSLO https://releases.hashicorp.com/terraform-provider-aws/$TERRAFORM_PROVIDER_AWS_VERSION/terraform-provider-aws_${TERRAFORM_PROVIDER_AWS_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-aws_*_linux_amd64.zip -d /usr/bin && \
    curl -sSLO https://releases.hashicorp.com/terraform-provider-fastly/$TERRAFORM_PROVIDER_FASTLY_VERSION/terraform-provider-fastly_${TERRAFORM_PROVIDER_FASTLY_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-fastly_*_linux_amd64.zip -d /usr/bin && \
    wget -q https://s3-eu-west-1.amazonaws.com/mmg-terraform-providers/terraform-provider-logentries_v${TERRAFORM_PROVIDER_LOGENTRIES_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-logentries_*_linux_amd64.zip -d /usr/bin && \
    curl -sSLO https://releases.hashicorp.com/terraform-provider-null/$TERRAFORM_PROVIDER_NULL_VERSION/terraform-provider-null_${TERRAFORM_PROVIDER_NULL_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-null_*_linux_amd64.zip -d /usr/bin && \
    curl -sSLO https://releases.hashicorp.com/terraform-provider-template/$TERRAFORM_PROVIDER_TEMPLATE_VERSION/terraform-provider-template_${TERRAFORM_PROVIDER_TEMPLATE_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-template_*_linux_amd64.zip -d /usr/bin && \
    wget -q https://github.com/paybyphone/terraform-provider-acme/releases/download/v${TERRAFORM_PROVIDER_ACME_VERSION}/terraform-provider-acme_v${TERRAFORM_PROVIDER_ACME_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-acme_*_linux_amd64.zip -d /usr/bin && \
    curl -sSLO https://releases.hashicorp.com/terraform-provider-external/$TERRAFORM_PROVIDER_EXTERNAL_VERSION/terraform-provider-external_${TERRAFORM_PROVIDER_EXTERNAL_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-external_*_linux_amd64.zip -d /usr/bin && \
    curl -sSLO https://releases.hashicorp.com/terraform-provider-tls/$TERRAFORM_PROVIDER_TLS_VERSION/terraform-provider-tls_${TERRAFORM_PROVIDER_TLS_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-tls*_linux_amd64.zip -d /usr/bin && \
    curl -sSLO https://releases.hashicorp.com/terraform-provider-datadog/$TERRAFORM_PROVIDER_DATADOG_VERSION/terraform-provider-datadog_${TERRAFORM_PROVIDER_DATADOG_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-datadog*_linux_amd64.zip -d /usr/bin && \
    rm -rf /tmp/* && \
    rm -rf /var/tmp/*


ENV PYTHONDONTWRITEBYTECODE donot

RUN pip install --no-cache-dir -r requirements.txt
ADD infra /infra
