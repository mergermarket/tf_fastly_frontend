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
- `caching` - (bool) - Whether to enable / forcefully disable caching (default: `true`)
- `force_ssl` - (bool) - Controls whether to redirect HTTP -> HTTPS (default: `true`)

### domain_name permutations

This module will actually configure two domain names which will be the entry point to the service - with `www` prefix and bare domain, as passed via the parameter.
On top of this, depending on environment, for `non-live` environments, $env prefix will be added to the domain.

Example full list of permutations for domain `domain.com` (i.e. you pass `domain.com` via `dns_domain` parameter) in all environments will be as following:

| Environment | Domain names configured in Fastly |
| `live` | `domain.com`, `www.domain.com` |
| `ci` | `ci.domain.com`, `ci-www.domain.com` |

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
