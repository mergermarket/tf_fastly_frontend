provider "logentries" {}

module "secretsmanager" {
  source   = "./modules/secretsmanager"
  run_data = "${var.run_data}"
  env      = "${var.env}"
}

locals {
  full_domain_name = "${var.env == "live" ? "" : format("%s-", var.env)}${var.domain_name}"

  tls_ca_cert = <<END
-----BEGIN CERTIFICATE-----
MIIESTCCAzGgAwIBAgITBn+UV4WH6Kx33rJTMlu8mYtWDTANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MTAyMjAwMDAwMFoXDTI1MTAxOTAwMDAwMFowRjEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEVMBMGA1UECxMMU2VydmVyIENB
IDFCMQ8wDQYDVQQDEwZBbWF6b24wggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEK
AoIBAQDCThZn3c68asg3Wuw6MLAd5tES6BIoSMzoKcG5blPVo+sDORrMd4f2AbnZ
cMzPa43j4wNxhplty6aUKk4T1qe9BOwKFjwK6zmxxLVYo7bHViXsPlJ6qOMpFge5
blDP+18x+B26A0piiQOuPkfyDyeR4xQghfj66Yo19V+emU3nazfvpFA+ROz6WoVm
B5x+F2pV8xeKNR7u6azDdU5YVX1TawprmxRC1+WsAYmz6qP+z8ArDITC2FMVy2fw
0IjKOtEXc/VfmtTFch5+AfGYMGMqqvJ6LcXiAhqG5TI+Dr0RtM88k+8XUBCeQ8IG
KuANaL7TiItKZYxK1MMuTJtV9IblAgMBAAGjggE7MIIBNzASBgNVHRMBAf8ECDAG
AQH/AgEAMA4GA1UdDwEB/wQEAwIBhjAdBgNVHQ4EFgQUWaRmBlKge5WSPKOUByeW
dFv5PdAwHwYDVR0jBBgwFoAUhBjMhTTsvAyUlC4IWZzHshBOCggwewYIKwYBBQUH
AQEEbzBtMC8GCCsGAQUFBzABhiNodHRwOi8vb2NzcC5yb290Y2ExLmFtYXpvbnRy
dXN0LmNvbTA6BggrBgEFBQcwAoYuaHR0cDovL2NydC5yb290Y2ExLmFtYXpvbnRy
dXN0LmNvbS9yb290Y2ExLmNlcjA/BgNVHR8EODA2MDSgMqAwhi5odHRwOi8vY3Js
LnJvb3RjYTEuYW1hem9udHJ1c3QuY29tL3Jvb3RjYTEuY3JsMBMGA1UdIAQMMAow
CAYGZ4EMAQIBMA0GCSqGSIb3DQEBCwUAA4IBAQCFkr41u3nPo4FCHOTjY3NTOVI1
59Gt/a6ZiqyJEi+752+a1U5y6iAwYfmXss2lJwJFqMp2PphKg5625kXg8kP2CN5t
6G7bMQcT8C8xDZNtYTd7WPD8UZiRKAJPBXa30/AbwuZe0GaFEQ8ugcYQgSn+IGBI
8/LwhBNTZTUVEWuCUUBVV18YtbAiPq3yXqMB48Oz+ctBWuZSkbvkNodPLamkB2g1
upRyzQ7qDn1X8nn8N8V7YJ6y68AtkHcNSRAnpTitxBKjtKPISLMVCx7i4hncxHZS
yLyKQXhw2W2Xs0qLeC1etA+jTGDK4UfLeC0SF7FSi8o5LL21L8IzApar2pR/
-----END CERTIFICATE-----
END
}

resource "fastly_service_v1" "fastly" {
  name = "${var.env}-${var.domain_name}"

  domain {
    name = "${local.full_domain_name}"
  }

  default_host = "${var.override_host == "true" ? local.full_domain_name : ""}"
  default_ttl  = 60

  backend {
    address               = "${var.backend_address}"
    name                  = "default backend"
    port                  = 443
    use_ssl               = "true"
    ssl_check_cert        = "${var.ssl_cert_check}"
    ssl_cert_hostname     = "${var.ssl_cert_hostname}"
    connect_timeout       = "${var.connect_timeout}"
    first_byte_timeout    = "${var.first_byte_timeout}"
    between_bytes_timeout = "${var.between_bytes_timeout}"
    shield                = "${var.shield}"
  }

  gzip {
    name          = "file extensions and content types"
    extensions    = ["css", "js"]
    content_types = ["text/html", "text/css", "application/json"]
  }

  request_setting {
    name             = "request-setting"
    force_ssl        = "${var.force_ssl}"
    bypass_busy_wait = "${var.bypass_busy_wait}"
  }

  # Override requests for /robots.txt for non-live environments
  response_object {
    name              = "override-robots.txt"
    status            = 200
    response          = "OK"
    content           = "${data.template_file.robotstxt.rendered}"
    content_type      = "text/plain"
    request_condition = "override-robots.txt-condition"
  }

  condition {
    name      = "override-robots.txt-condition"
    type      = "REQUEST"
    priority  = 5
    statement = "req.url ${var.env == "live" ? "!~ \".*\"" : "~ \"^/robots.txt\""}"
  }

  response_object {
    name            = "error-response-404"
    status          = 404
    response        = "Not Found"
    content         = "${var.not_found_response}"
    content_type    = "text/html"
    cache_condition = "response-404-condition"
  }

  condition {
    name      = "response-404-condition"
    type      = "CACHE"
    priority  = 5
    statement = "${var.not_found_response == "" ? "now.sec == \"\"" : "beresp.status == 404 && req.http.Cookie:viewerror != \"true\""}"
  }

  response_object {
    name            = "error-response-500"
    status          = 500
    response        = "Server Error"
    content         = "${var.error_response}"
    content_type    = "text/html"
    cache_condition = "response-500-condition"
  }

  condition {
    name      = "response-500-condition"
    type      = "CACHE"
    priority  = 5
    statement = "${var.error_response == "" ? "now.sec == \"\"" : "beresp.status == 500 && req.http.Cookie:viewerror != \"true\""}"
  }

  # 503 error handling
  response_object {
    name            = "error-response-503"
    status          = 503
    response        = "Service Unavailable"
    content         = "${var.proxy_error_response}"
    content_type    = "text/html"
    cache_condition = "response-503-condition"
  }

  condition {
    name      = "response-503-condition"
    type      = "CACHE"
    priority  = 5
    statement = "beresp.status == 503 && req.http.Cookie:viewerror != \"true\""
  }

  # 502 error handling
  response_object {
    name            = "error-response-502"
    status          = 502
    response        = "Bad Gateway"
    content         = "${var.proxy_error_response}"
    content_type    = "text/html"
    cache_condition = "response-502-condition"
  }

  condition {
    name      = "response-502-condition"
    type      = "CACHE"
    priority  = 5
    statement = "beresp.status == 502 && req.http.Cookie:viewerror != \"true\""
  }

  condition {
    name      = "surrogate-key-condition"
    type      = "CACHE"
    priority  = 10
    statement = "beresp.http.${var.surrogate_key_name} != \"\""
  }

  condition {
    name      = "syslog-no-shield-condition"
    type      = "RESPONSE"
    priority  = 10
    statement = "!req.http.Fastly-FF"
  }

  # Add the client ip
  header {
    name        = "Add X-Client-IP header"
    source      = "req.http.Fastly-Client-IP"
    destination = "http.X-Client-IP"
    type        = "request"
    action      = "set"
  }

  # Sanitise HTTP headers
  header {
    name        = "Remove X-Powered-By header"
    destination = "http.X-Powered-By"
    type        = "cache"
    action      = "delete"
  }

  header {
    name        = "Obfuscate Server header"
    destination = "http.Server"
    type        = "cache"
    action      = "set"
    source      = "\"LHC\""
  }

  header {
    name            = "Surrogate Key to Amazon"
    destination     = "http.Surrogate-Key"
    type            = "cache"
    action          = "set"
    source          = "beresp.http.${var.surrogate_key_name}"
    cache_condition = "surrogate-key-condition"
    priority        = 10
  }

  syslog {
    name               = "${local.full_domain_name}-syslog"
    address            = "intake.logs.datadoghq.com"
    port               = "10516"
    message_type       = "blank"
    format             = "${module.secretsmanager.datadog_api_key} ${replace(data.local_file.container_definitions.content, "\n", "")}"
    format_version     = "2"
    use_tls            = true
    tls_hostname       = "intake.logs.datadoghq.com"
    tls_ca_cert        = "${local.tls_ca_cert}"
    response_condition = "syslog-no-shield-condition"
  }

  vcl {
    name    = "custom_vcl"
    content = "${data.template_file.custom_vcl.rendered}"
    main    = true
  }

  force_destroy = true
}

data "template_file" "custom_vcl" {
  template = "${file("${path.module}/custom.vcl")}"

  vars {
    proxy_error_response        = "${var.proxy_error_response}"
    custom_vcl_backends         = "${var.custom_vcl_backends}"
    custom_vcl_recv             = "${var.custom_vcl_recv}"
    custom_vcl_recv_no_shield   = "${var.custom_vcl_recv_no_shield}"
    custom_vcl_recv_shield_only = "${var.custom_vcl_recv_shield_only}"
    custom_vcl_error            = "${var.custom_vcl_error}"
    custom_vcl_deliver          = "${var.custom_vcl_deliver}"
    vcl_recv_default_action     = "${var.caching == "true" ? "lookup" : "pass"}"
  }
}

# resource performing bare-domain redirection to prefix; only for live
resource "fastly_service_v1" "fastly_bare_domain_redirection" {
  name  = "${var.bare_redirect_domain_name}-redirection"
  count = "${var.bare_redirect_domain_name != "" ? 1 : 0}"

  domain {
    name = "${var.bare_redirect_domain_name}"
  }

  backend {
    address               = "${var.backend_address}"
    name                  = "default backend"
    port                  = 443
    ssl_check_cert        = "false"
    connect_timeout       = "${var.connect_timeout}"
    first_byte_timeout    = "${var.first_byte_timeout}"
    between_bytes_timeout = "${var.between_bytes_timeout}"
  }

  response_object {
    name     = "redirect_bare_domain_to_prefix"
    status   = 301
    response = "Moved Permanently"
  }

  header {
    name        = "redirect_bare_domain_to_prefix"
    destination = "http.Location"
    type        = "response"
    action      = "set"
    source      = "\"https://${local.full_domain_name}\" + req.url"
  }

  syslog {
    name           = "${local.full_domain_name}"
    address        = "intake.logs.datadoghq.com"
    port           = "10516"
    message_type   = "blank"
    format         = "${module.secretsmanager.datadog_api_key} '%t %u %v \"%r\" %>s %b %h'"
    format_version = "2"
    use_tls        = true
    tls_hostname   = "intake.logs.datadoghq.com"
    tls_ca_cert    = "${local.tls_ca_cert}"
  }
}

data "local_file" "container_definitions" {
  filename = "${path.module}/dd_log_format.json"
}
