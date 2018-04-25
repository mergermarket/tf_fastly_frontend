# fixture
# generate fastly config
module "fastly" {
  source = "../.."

  domain_name               = "${var.domain_name}"
  backend_address           = "${var.backend_address}"
  env                       = "${var.env}"
  bare_redirect_domain_name = "${var.bare_redirect_domain_name}"
  proxy_error_response      = "${var.proxy_error_response}"
  custom_vcl_backends       = "${var.custom_vcl_backends}"
  custom_vcl_recv           = "${var.custom_vcl_recv}"
  custom_vcl_error          = "${var.custom_vcl_error}"
}

module "fastly_custom_timeouts" {
  source = "../.."

  domain_name           = "${var.domain_name}"
  backend_address       = "${var.backend_address}"
  env                   = "${var.env}"
  connect_timeout       = "${var.connect_timeout}"
  first_byte_timeout    = "${var.first_byte_timeout}"
  between_bytes_timeout = "${var.between_bytes_timeout}"
}

module "fastly_disable_caching" {
  source = "../.."

  domain_name     = "${var.domain_name}"
  backend_address = "${var.backend_address}"
  env             = "${var.env}"
  caching         = "${var.caching}"
}

module "fastly_disable_force_ssl" {
  source = "../.."

  domain_name     = "${var.domain_name}"
  backend_address = "${var.backend_address}"
  env             = "${var.env}"
  force_ssl       = "${var.force_ssl}"
}

module "fastly_ssl_cert_hostname" {
  source = "../.."

  domain_name       = "${var.domain_name}"
  backend_address   = "${var.backend_address}"
  env               = "${var.env}"
  ssl_cert_hostname = "${var.ssl_cert_hostname}"
}

module "fastly_set_shield" {
  source = "../.."

  domain_name     = "${var.domain_name}"
  backend_address = "${var.backend_address}"
  env             = "${var.env}"
  shield          = "${var.shield}"
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

variable "custom_vcl_error" {
  default = ""
}

variable "shield" {
  default = ""
}
