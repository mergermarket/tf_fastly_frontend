Fastly Frontend terraform module
================================

[![Build Status](https://travis-ci.org/mergermarket/tf_fastly_frontend.svg?branch=master)](https://travis-ci.org/mergermarket/tf_fastly_frontend)

This module creates Fastly Frontend including some conditions, like:
- conditionally forcing SSL
- conditionally disabling caching

Also, some HTTP headers obfuscation will be configured (http.Server, etc.)

Request logging is deployed by default for all Fastly configurations - Fastly uses Real-Time Logging feature to push logs directly to Datadog.

**NOTE:** If you want to use HTTPS you need to set up SSL Certification beforehand

Module Input Variables
----------------------

- `domain_name` - (string) - **REQUIRED** - The full domain name for your website in live, including any prefix (e.g. `www.my-site.com`).
- `backend_address` - (string) - **REQUIRED** - Backend address to service requests for your domains
- `env` - (string) - **REQUIRED** - Environment name - for non-live environments, will be prefixed with a hyphen onto the start of the domain name. used to build name of resources and conditionally enable/disable certain features of the module
- `bare_redirect_domain_name` - (string) - If set, a service will be created in live to redirect this bare domain to the prefixed version - for example you might set this value to `my-site.com` in order to redirect users to `www.my-site.com` (default `""`, i.e. will not be used)
- `caching` - (bool) - Whether to enable / forcefully disable caching (default: `true`)
- `force_ssl` - (bool) - Controls whether to redirect HTTP -> HTTPS (default: `true`)
- `ssl_cert_check` - (bool) - Check the backend cert is valid - warning disabling this makes you vulnerable to a man-in-the-middle imporsonating your backend (default `true`).
- `ssl_cert_hostname` - (string) - The hostname to validate the certificate presented by the backend against (default `""`).
- `connect_timeout` - (string) - How long to wait for a timeout in milliseconds (default: `5000`)
- `first_byte_timeout` - (string) - How long to wait for the first bytes in milliseconds (default: `60000`)
- `between_bytes_timeout` - (string) - How long to wait between bytes in milliseconds (default: `30000`)
- `proxy_error_response` - (string) - The html error document to send for a proxy error - 502/503 from backend, or no response from backend at all.
- `override_host` - (bool) - Whether to enable / disable overriding the host of the request (default: `true`)

Usage
-----

```hcl
module "fastly" {
  source = "github.com/mergermarket/tf_fastly_frontend"

  domain_name               = "www.domain.com"
  backend_address           = "aws-alb-address.com"
  env                       = "ci"
  bare_redirect_domain_name = "domain.com"
}
```
