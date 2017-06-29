# fixture
# generate fastly config
module "fastly" {
  source = "../.."

  domain_name               = "${var.domain_name}"
  backend_address           = "${var.backend_address}"
  env                       = "${var.env}"
  bare_redirect_domain_name = "${var.bare_redirect_domain_name}"
  error_response_502        = "${var.error_response_502}"
  error_response_503        = "${var.error_response_503}"
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

variable "error_response_503" {
  default = "abc"
}

variable "error_response_502" {
  default = "cba"
}
