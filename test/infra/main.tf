# fixture
# generate fastly config
module "fastly" {
  source = "../.."

  domain_name     = "${var.domain_name}"
  backend_address = "${var.backend_address}"
  env             = "${var.env}"
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

variable "backend_address" {}

variable "env" {}

variable "caching" {
  default = "true"
}

variable "force_ssl" {
  default = "true"
}

variable "connect_timeout" {
  default = ""
}

variable "first_byte_timeout" {
  default = ""
}

variable "between_bytes_timeout" {
  default = ""
}
