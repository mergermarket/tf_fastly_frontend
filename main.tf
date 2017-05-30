resource "fastly_service_v1" "fastly" {
  name = "${var.env}-${var.domain_name}"

  domain {
    name = "${var.env == "live" ? "www." : format("%s-www.", var.env)}${var.domain_name}"
  }

  domain {
    name = "${var.env == "live" ? "" : format("%s.", var.env)}${var.domain_name}"
  }

  default_host = "${var.env == "live" ? "www." : format("%s-www.", var.env)}${var.domain_name}"
  default_ttl  = 60

  backend {
    address               = "${var.backend_address}"
    name                  = "default backend"
    port                  = 443
    ssl_check_cert        = "false"
    connect_timeout       = 5000
    first_byte_timeout    = 60000
    between_bytes_timeout = 30000
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
