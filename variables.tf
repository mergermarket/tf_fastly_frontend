# variables that must be passed to the module
variable "domain_name" {
  type        = "string"
  description = "Domain name to use for this Fastly configuration"
}

variable "bare_redirect_domain_name" {
  type        = "string"
  default     = ""
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

variable "ssl_cert_check" {
  type        = "string"
  description = "Should the backend SSL cert be checked - warning turning this off may reduce security."
  default     = "true"
}

variable "ssl_cert_hostname" {
  type        = "string"
  description = "The hostname to validate the certificate presented by the backend against."
  default     = ""
}

variable "error_response_503" {
  type        = "string"
  description = "The html error document to send when we get a service unavailable from the backend."

  default = <<EOF
<!DOCTYPE html>
<html>
  <head>
    <title>503 Service Unavailable</title>
  </head>
  <body>
    <h1>Service Unavailable (503)</h1>
    <p>
      The site you requested is currently unavailable.
    </p>
  </body>
</html>
EOF
}

variable "error_response_502" {
  type        = "string"
  description = "The html error document to send when we get a bad gateway from the backend."

  default = <<EOF
<!DOCTYPE html>
<html>
  <head>
    <title>502 Bad Gateway</title>
  </head>
  <body>
    <h1>Bad Gateway (502)</h1>
    <p>
      The site you requested is currently unavailable.
    </p>
  </body>
</html>
EOF
}
