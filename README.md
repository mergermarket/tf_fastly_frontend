Fastly Frontend terraform module
================================

This module creates Fastly Frontend including some conditions, like:
- conditionally forcing SSL
- conditionally disabling caching

Also, some HTTP headers obfuscation will be configured (http.Server, etc.)

**NOTE:** If you want to use HTTPS you need to set up SSL Certification beforehand

Module Input Variables
----------------------

- `domain_name` - (string) - **REQUIRED** - Domain name to serve as entry points for your service
- `backend_address` - (string) - **REQUIRED** - Backend address to service requests for your domains
- `env` - (string) - **REQUIRED** - Environment name - used to build name of resources and conditionally enable/disable certain features of the module
- `prefix` - (string) - Domain prefix (default: `www`)
- `caching` - (bool) - Whether to enable / forcefully disable caching (default: `true`)
- `force_ssl` - (bool) - Controls whether to redirect HTTP -> HTTPS (default: `true`)
- `ssl_cert_check` - (bool) - Check the backend cert is valid - warning disabling this makes you vulnerable to a man-in-the-middle imporsonating your backend (default `true`).
- `ssl_cert_hostname` - (string) - The hostname to validate the certificate presented by the backend against (default `""`).
- `connect_timeout` - (string) - How long to wait for a timeout in milliseconds (default: `5000`)
- `first_byte_timeout` - (string) - How long to wait for the first bytes in milliseconds (default: `60000`)
- `between_bytes_timeout` - (string) - How long to wait between bytes in milliseconds (default: `30000`)

Usage
-----

```hcl
module "fastly" {
  source = "../.."

  domain_name     = "domain.com"
  backend_address = "aws-alb-address.com"
  env             = "ci"
}
```
