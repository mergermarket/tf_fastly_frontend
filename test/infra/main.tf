# fixture
# generate fastly config
module "fastly" {
  source = "../.."

  domain_name               = "${var.domain_name}"
  backend_address           = "${var.backend_address}"
  env                       = "${var.env}"
  bare_redirect_domain_name = "${var.bare_redirect_domain_name}"
  proxy_error_response      = "${var.proxy_error_response}"
  le_logset_id              = "${var.le_logset_id}"
}

module "fastly_custom_timeouts" {
  source = "../.."

  domain_name           = "${var.domain_name}"
  backend_address       = "${var.backend_address}"
  env                   = "${var.env}"
  connect_timeout       = "${var.connect_timeout}"
  first_byte_timeout    = "${var.first_byte_timeout}"
  between_bytes_timeout = "${var.between_bytes_timeout}"
  le_logset_id          = "${var.le_logset_id}"
}

module "fastly_disable_caching" {
  source = "../.."

  domain_name     = "${var.domain_name}"
  backend_address = "${var.backend_address}"
  env             = "${var.env}"
  caching         = "${var.caching}"
  le_logset_id    = "${var.le_logset_id}"
}

module "fastly_disable_force_ssl" {
  source = "../.."

  domain_name     = "${var.domain_name}"
  backend_address = "${var.backend_address}"
  env             = "${var.env}"
  force_ssl       = "${var.force_ssl}"
  le_logset_id    = "${var.le_logset_id}"
}

module "fastly_ssl_cert_hostname" {
  source = "../.."

  domain_name       = "${var.domain_name}"
  backend_address   = "${var.backend_address}"
  env               = "${var.env}"
  ssl_cert_hostname = "${var.ssl_cert_hostname}"
  le_logset_id      = "${var.le_logset_id}"
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

variable "le_logset_id" {
  default = "123"
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
