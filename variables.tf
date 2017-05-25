# variables that must be passed to the module
variable "domain_name" {
  type        = "string"
  description = "Domain name to use for this Fastly configuration"
}

variable "backend_address" {
  type        = "string"
  description = "Backend address to forward all requests to"
}

variable "env" {
  type        = "string"
  description = "Environment name"
}

# optional variables
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
