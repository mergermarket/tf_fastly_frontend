# variables that must be passed to the module
variable "domain_name" {
  type        = "string"
  description = "Domain name to use for this Fastly configuration"
}

variable "bare_redirect_domain_name" {
  type = "string"
  default = ""
  description = "If set then an additional service will be created to redirect the zone apex (bare domain) to the domain - i.e. add the www."
}

variable "backend_address" {
  type        = "string"
  description = "Backend address to forward all requests to"
}

variable "env" {
  type        = "string"
  description = "Environment name"
}

variable "caching" {
  type        = "string"
  description = "Whether to or not disable caching on Fastly (default: true)"
  default     = "true"
}

variable "force_ssl" {
  type        = "string"
  description = "Whether or not to force SSL (redirect requests to HTTP to HTTPS)"
  default     = "true"
}

variable "connect_timeout" {
  type        = "string"
  description = ""
  default     = 5000
}

variable "first_byte_timeout" {
  type        = "string"
  description = ""
  default     = 60000
}

variable "between_bytes_timeout" {
  type        = "string"
  description = ""
  default     = 30000
}
