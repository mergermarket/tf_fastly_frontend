# fixture
# generate fastly config
# configure provider to not try too hard talking to AWS API
provider "aws" {
  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_get_ec2_platforms      = true
  skip_region_validation      = true
  skip_requesting_account_id  = true
  max_retries                 = 1
  access_key                  = "a"
  secret_key                  = "a"
  region                      = "eu-west-1"
}

module "fastly" {
  source = "../.."

  domain_name                 = "${var.domain_name}"
  backend_address             = "${var.backend_address}"
  env                         = "${var.env}"
  bare_redirect_domain_name   = "${var.bare_redirect_domain_name}"
  proxy_error_response        = "${var.proxy_error_response}"
  custom_vcl_backends         = "${var.custom_vcl_backends}"
  custom_vcl_recv             = "${var.custom_vcl_recv}"
  custom_vcl_recv_no_shield   = "${var.custom_vcl_recv_no_shield}"
  custom_vcl_recv_shield_only = "${var.custom_vcl_recv_shield_only}"
  custom_vcl_error            = "${var.custom_vcl_error}"
  custom_vcl_deliver          = "${var.custom_vcl_deliver}"
  run_data                    = false
}

module "fastly_custom_timeouts" {
  source = "../.."

  domain_name           = "${var.domain_name}"
  backend_address       = "${var.backend_address}"
  env                   = "${var.env}"
  connect_timeout       = "${var.connect_timeout}"
  first_byte_timeout    = "${var.first_byte_timeout}"
  between_bytes_timeout = "${var.between_bytes_timeout}"
  run_data              = false
}

module "fastly_disable_caching" {
  source = "../.."

  domain_name     = "${var.domain_name}"
  backend_address = "${var.backend_address}"
  env             = "${var.env}"
  caching         = "${var.caching}"
  run_data        = false
}

module "fastly_disable_force_ssl" {
  source = "../.."

  domain_name     = "${var.domain_name}"
  backend_address = "${var.backend_address}"
  env             = "${var.env}"
  force_ssl       = "${var.force_ssl}"
  run_data        = false
}

module "fastly_ssl_cert_hostname" {
  source = "../.."

  domain_name       = "${var.domain_name}"
  backend_address   = "${var.backend_address}"
  env               = "${var.env}"
  ssl_cert_hostname = "${var.ssl_cert_hostname}"
  run_data          = false
}

module "fastly_set_shield" {
  source = "../.."

  domain_name     = "${var.domain_name}"
  backend_address = "${var.backend_address}"
  env             = "${var.env}"
  shield          = "${var.shield}"
  run_data        = false
}

module "fastly_set_surrogate_key" {
  source = "../.."

  domain_name        = "${var.domain_name}"
  backend_address    = "${var.backend_address}"
  env                = "${var.env}"
  surrogate_key_name = "${var.surrogate_key_name}"
  run_data           = false
}

# variables
variable "domain_name" {}

variable "bare_redirect_domain_name" {
  default = ""
}

variable "backend_address" {}

variable "env" {}

variable "caching" {
  default = "true"
}

variable "force_ssl" {
  default = "true"
}

variable "connect_timeout" {
  default = 123
}

variable "first_byte_timeout" {
  default = 456
}

variable "between_bytes_timeout" {
  default = 789
}

variable "proxy_error_response" {
  default = "abc"
}

variable "ssl_cert_hostname" {
  default = ""
}

variable "custom_vcl_backends" {
  default = ""
}

variable "custom_vcl_recv" {
  default = ""
}

variable "custom_vcl_recv_no_shield" {
  default = ""
}

variable "custom_vcl_recv_shield_only" {
  default = ""
}

variable "custom_vcl_error" {
  default = ""
}

variable "custom_vcl_deliver" {
  default = ""
}

variable "shield" {
  default = ""
}

variable "surrogate_key_name" {
  default = ""
}
