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

variable "le_logset_parent_name" {
  description = "Logentries Logset Name under which Logs will be created"
  type        = "string"
  default     = "Fastly"
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

variable "proxy_error_response" {
  type        = "string"
  description = "The html error document to send for a proxy error - 502/503 from backend, or no response from backend at all."

  default = <<EOF
<!DOCTYPE html>
<html>
  <head>
    <title>Service Unavailable</title>
  </head>
  <body>
    <h1>Service Unavailable</h1>
    <p>
      The site you requested is currently unavailable.
    </p>
  </body>
</html>
EOF
}

variable "not_found_response" {
  type        = "string"
  description = "The html error document to send for a not found error"
  default     = ""
}

variable "error_response" {
  type        = "string"
  description = "The html error document to send for a not found error"
  default     = ""
}

variable "custom_vcl_backends" {
  type        = "string"
  description = "Custom VCL to add at the top level (e.g. for defining backends)"
  default     = ""
}

variable "custom_vcl_recv" {
  type        = "string"
  description = "Custom VCL to add to the vcl_recv sub after the Fastly hook - this will run regardess of whether running on a shield node"
  default     = ""
}

variable "custom_vcl_recv_shield_only" {
  type        = "string"
  description = "Custom VCL to add to the vcl_recv sub after the Fastly hook, only on shield nodes"
  default     = ""
}

variable "custom_vcl_recv_no_shield" {
  type        = "string"
  description = "Custom VCL to add to the vcl_recv sub after the Fastly hook, but not on shield nodes"
  default     = ""
}

variable "custom_vcl_error" {
  type        = "string"
  description = "Custom VCL to add to the vcl_error sub after the Fastly hook"
  default     = ""
}

variable "custom_vcl_deliver" {
  type        = "string"
  description = "Custom VCL to add to the vcl_deliver sub after the Fastly hook"
  default     = ""
}

variable "bypass_busy_wait" {
  type        = "string"
  description = "Disable collapsed forwarding, so you don't wait for other objects to origin."
  default     = "false"
}

variable "shield" {
  type        = "string"
  description = "PoP to use as an origin shield (e.g. london-uk for Slough)."
  default     = ""
}

variable "surrogate_key_name" {
  type        = "string"
  description = "Fastly surrogate key name"
  default     = "default-surrogate-key"
}

variable "run_data" {
  description = "Used to switch off data resources when unit testing"
  default     = true
}

variable "override_host" {
  description = "Used to enable or disable setting of default_host (Override host in UI) value"
  default     = "true"
}
