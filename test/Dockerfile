FROM python:3-alpine
COPY requirements.txt .

ENV TERRAFORM_VERSION=0.10.0-rc1

ENV TERRAFORM_PROVIDER_AWS_VERSION=0.1.3
ENV TERRAFORM_PROVIDER_FASTLY_VERSION=0.1.2_le-support
ENV TERRAFORM_PROVIDER_NULL_VERSION=0.1.0
ENV TERRAFORM_PROVIDER_TEMPLATE_VERSION=0.1.1
ENV TERRAFORM_PROVIDER_ACME_VERSION=0.3.0
ENV TERRAFORM_PROVIDER_LOGENTRIES_VERSION=0.1.0

ENV PYTHONDONTWRITEBYTECODE donot

RUN apk update && apk add ca-certificates curl git openssl wget && \
    update-ca-certificates && \
    cd /tmp && \
    wget -q https://releases.hashicorp.com/terraform/$TERRAFORM_VERSION/terraform_${TERRAFORM_VERSION}_linux_amd64.zip && \
        unzip terraform_*_linux_amd64.zip -d /usr/bin && \
    wget -q https://releases.hashicorp.com/terraform-provider-aws/${TERRAFORM_PROVIDER_AWS_VERSION}/terraform-provider-aws_${TERRAFORM_PROVIDER_AWS_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-aws_*_linux_amd64.zip -d /usr/bin && \
    wget -q https://s3-eu-west-1.amazonaws.com/mmg-terraform-providers/terraform-provider-fastly_v${TERRAFORM_PROVIDER_FASTLY_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-fastly_*_linux_amd64.zip -d /usr/bin && \
    wget -q https://releases.hashicorp.com/terraform-provider-null/${TERRAFORM_PROVIDER_NULL_VERSION}/terraform-provider-null_${TERRAFORM_PROVIDER_NULL_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-null_*_linux_amd64.zip -d /usr/bin && \
    wget -q https://releases.hashicorp.com/terraform-provider-template/${TERRAFORM_PROVIDER_TEMPLATE_VERSION}/terraform-provider-template_${TERRAFORM_PROVIDER_TEMPLATE_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-template_*_linux_amd64.zip -d /usr/bin && \
    wget -q https://releases.hashicorp.com/terraform-provider-logentries/${TERRAFORM_PROVIDER_LOGENTRIES_VERSION}/terraform-provider-logentries_${TERRAFORM_PROVIDER_LOGENTRIES_VERSION}_linux_amd64.zip && \
            unzip terraform-provider-logentries_*_linux_amd64.zip -d /usr/bin && \
    wget -q https://github.com/paybyphone/terraform-provider-acme/releases/download/v${TERRAFORM_PROVIDER_ACME_VERSION}/terraform-provider-acme_v${TERRAFORM_PROVIDER_ACME_VERSION}_linux_amd64.zip && \
        unzip terraform-provider-acme_*_linux_amd64.zip -d /usr/bin && \
    rm -rf /tmp/* /var/cache/apk/* /var/tmp/*

RUN pip install --no-cache-dir -r requirements.txt
ADD infra /infra
