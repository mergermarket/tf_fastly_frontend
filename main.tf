resource "fastly_service_v1" "fastly" {
  name = "${var.env}-${var.domain_name}"

  domain {
    name = "${var.env == "live" ? "" : format("%s-", var.env)}${var.domain_name}"
  }

  default_host = "${var.env == "live" ? "" : format("%s-", var.env)}${var.domain_name}"
  default_ttl  = 60

  backend {
    address               = "${var.backend_address}"
    name                  = "default backend"
    port                  = 443
    ssl_check_cert        = "false"
    connect_timeout       = "${var.connect_timeout}"
    first_byte_timeout    = "${var.first_byte_timeout}"
    between_bytes_timeout = "${var.between_bytes_timeout}"
  }

  gzip {
    name          = "file extensions and content types"
    extensions    = ["css", "js"]
    content_types = ["text/html", "text/css", "application/json"]
  }

  # Set force-miss (disables caching) and force-ssl (enables redirect from HTTP
  # -> HTTPS for all requests) settings
  request_setting {
    name              = "disable caching"
    request_condition = "all_urls"
    force_miss        = "${var.caching == "false" ? true : false}"
    force_ssl         = "${var.force_ssl}"
  }

  condition {
    name      = "all_urls"
    priority  = "10"
    statement = "req.url ~ \".*\""
    type      = "REQUEST"
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

  # 503 error handling
  response_object {
    name            = "error-response-503",
    status          = 503,
    response        = "Service Unavailable",
    content         = "${var.error_response_503}",
    content_type    = "text/html"
    cache_condition = "response-503-condition"
  }

  condition {
    name      = "response-503-condition"
    type      = "CACHE"
    priority  = 5
    statement = "beresp.status == 503"
  }

  # 502 error handling
  response_object {
    name            = "error-response-502",
    status          = 502,
    response        = "Bad Gateway",
    content         = "${var.error_response_502}",
    content_type    = "text/html"
    cache_condition = "response-502-condition"
  }

  condition {
    name      = "response-502-condition"
    type      = "CACHE"
    priority  = 5
    statement = "beresp.status == 502"
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

  force_destroy = true
}

# resource performing bare-domain redirection to prefix; only for live
resource "fastly_service_v1" "fastly_bare_domain_redirection" {
  name  = "${var.domain_name}-redirection"
  count = "${var.env == "live" && var.bare_redirect_domain_name != "" ? 1 : 0}"

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
    name              = "redirect_bare_domain_to_prefix"
    status            = 301
    response          = "Moved Permanently"
    request_condition = "all_urls"
  }

  header {
    name              = "redirect_bare_domain_to_prefix"
    destination       = "http.Location"
    type              = "response"
    action            = "set"
    source            = "\"https://${var.domain_name}\" + req.url"
    request_condition = "all_urls"
  }

  condition {
    name      = "all_urls"
    type      = "REQUEST"
    priority  = 5
    statement = "req.url ~ \".*\""
  }
}
