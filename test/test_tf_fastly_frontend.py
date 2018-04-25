import unittest
import os
import re
from subprocess import check_call, check_output

cwd = os.getcwd()

"""
Takes a template (i.e. what you'd call `.format(...)` on, and returns a regex
to to match it:

    print(re.match(
        template_to_re("hello {name}"),
        "hello world"
    ).group("name"))
    # prints "world"

"""


def template_to_re(t):
    seen = dict()

    def pattern(placeholder, open_curly, close_curly, text):
        if text is not None:
            return re.escape(text)
        elif open_curly is not None:
            return r'\{'
        elif close_curly is not None:
            return r'\}'
        elif seen.get(placeholder):
            return '(?P={})'.format(placeholder)
        else:
            seen[placeholder] = True
            return '(?P<{}>.*?)'.format(placeholder)

    return "".join([
        pattern(*match.groups())
        for match in re.finditer(r'{([\w_]+)}|(\{\{)|(\}\})|([^{}]+)', t)
    ])


class TestTFFastlyFrontend(unittest.TestCase):

    def setUp(self):
        check_call(['terraform', 'init', 'test/infra'])
        check_call(['terraform', 'get', 'test/infra'])

    def _env_for_check_output(self, fastly_api_key):
        env = os.environ.copy()
        env.update({
            'FASTLY_API_KEY': fastly_api_key
        })
        return env

    def test_create_fastly_service(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(template_to_re("""
      domain.#:                                     "1"
      domain.{ident}.comment:                    ""
      domain.{ident}.name:                       "ci-www.domain.com"
        """.strip()), output)

        assert """
Plan: 2 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_fastly_logging_config(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(template_to_re("""
      logentries.#:                                 "1"
      logentries.~{ident}.format:                "%h %l %u %t %r %>s"
      logentries.~{ident}.format_version:        "1"
      logentries.~{ident}.name:                  "ci-www.domain.com"
      logentries.~{ident}.port:                  "20000"
      logentries.~{ident}.response_condition:    ""
        """.strip()), output) # noqa

        assert re.search(template_to_re("""
      logentries.~{ident}.use_tls:               "true"
        """.strip()), output) # noqa

        assert re.search(template_to_re("""
  + module.fastly.logentries_log.logs
        """.strip()), output) # noqa

        assert re.search(template_to_re("""
      name:                                         "ci-www.domain.com"
      retention_period:                             "ACCOUNT_DEFAULT"
      source:                                       "token"
      token:                                        <computed>
        """.strip()), output) # noqa

    def test_create_fastly_service_creates_redirection(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'bare_redirect_domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=any',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert """
+ module.fastly.fastly_service_v1.fastly
        """.strip() in output

        assert re.search(template_to_re("""
      domain.#:                                     "1"
      domain.{ident}.comment:                     ""
      domain.{ident}.name:                        "any-www.domain.com"
        """.strip()), output)

        assert """
+ module.fastly.fastly_service_v1.fastly_bare_domain_redirection
        """.strip() in output

        assert re.search(template_to_re("""
      header.{ident}.source:                     "\\"https://any-www.domain.com\\" + req.url"
        """.strip()), output) # noqa

        assert """
Plan: 3 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_delete_x_powered_by_header(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(template_to_re("""
      header.#:                                     "2"
      header.{ident}.action:                     "delete"
      header.{ident}.cache_condition:            ""
      header.{ident}.destination:                "http.X-Powered-By"
      header.{ident}.ignore_if_set:              "false"
      header.{ident}.name:                       "Remove X-Powered-By header"
      header.{ident}.priority:                   "100"
      header.{ident}.regex:                      <computed>
      header.{ident}.request_condition:          ""
      header.{ident}.response_condition:         ""
      header.{ident}.source:                     <computed>
      header.{ident}.substitution:               <computed>
      header.{ident}.type:                       "cache"
        """.strip()), output)

    def test_obfuscate_server_header(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(template_to_re("""
      header.{ident}.action:                     "set"
      header.{ident}.cache_condition:            ""
      header.{ident}.destination:                "http.Server"
      header.{ident}.ignore_if_set:              "false"
      header.{ident}.name:                       "Obfuscate Server header"
      header.{ident}.priority:                   "100"
      header.{ident}.regex:                      <computed>
      header.{ident}.request_condition:          ""
      header.{ident}.response_condition:         ""
      header.{ident}.source:                     "\\"LHC\\""
      header.{ident}.substitution:               <computed>
      header.{ident}.type:                       "cache"
        """.strip()), output)

    def test_override_robots_for_non_live_environments(self):
        # given

        # when
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert re.search(template_to_re("""
      response_object.{ident}.cache_condition:   ""
      response_object.{ident}.content:           "User-agent: *\\nDisallow: /\\n"
      response_object.{ident}.content_type:      "text/plain"
      response_object.{ident}.name:              "override-robots.txt"
      response_object.{ident}.request_condition: "override-robots.txt-condition"
      response_object.{ident}.response:          "OK"
      response_object.{ident}.status:            "200"

        """.strip()), output) # noqa

        assert re.search(template_to_re("""
      condition.{ident}.name:                     "override-robots.txt-condition"
      condition.{ident}.priority:                 "5"
      condition.{ident}.statement:                "req.url ~ \\"^/robots.txt\\""
      condition.{ident}.type:                     "REQUEST"
        """.strip()), output) # noqa

    def test_force_ssl_enabled_by_default(self):
        # given

        # when
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert re.search(template_to_re("""
      request_setting.#:                            "1"
      request_setting.{ident}.action:            ""
      request_setting.{ident}.bypass_busy_wait:  "false"
      request_setting.{ident}.default_host:      ""
      request_setting.{ident}.force_miss:        ""
      request_setting.{ident}.force_ssl:         "true"
      request_setting.{ident}.geo_headers:       ""
      request_setting.{ident}.hash_keys:         ""
      request_setting.{ident}.max_stale_age:     ""
      request_setting.{ident}.name:              "request-setting"
      request_setting.{ident}.request_condition: ""
      request_setting.{ident}.timer_support:     ""
      request_setting.{ident}.xff:               "append"
        """.strip()), output) # noqa

    def test_caching_enabled_by_default(self):
        # given

        # when
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        assert re.search(template_to_re("""
      cache_setting.#:                              "1"
      cache_setting.{ident}.action:              "cache"
      cache_setting.{ident}.cache_condition:     ""
      cache_setting.{ident}.name:                "cache-setting"
      cache_setting.{ident}.stale_ttl:           ""
      cache_setting.{ident}.ttl:                 ""
        """.strip()), output) # noqa

    def test_disable_caching(self):
        # when
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'caching=false',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly_disable_caching',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert re.search(template_to_re("""
      cache_setting.#:                              "1"
      cache_setting.{ident}.action:              "pass"
      cache_setting.{ident}.cache_condition:     ""
      cache_setting.{ident}.name:                "cache-setting"
      cache_setting.{ident}.stale_ttl:           ""
      cache_setting.{ident}.ttl:                 ""
        """.strip()), output) # noqa

    def test_disable_force_ssl(self):
        # when
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'force_ssl=false',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly_disable_force_ssl',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert re.search(template_to_re("""
      request_setting.#:                            "1"
      request_setting.{ident}.action:            ""
      request_setting.{ident}.bypass_busy_wait:  "false"
      request_setting.{ident}.default_host:      ""
      request_setting.{ident}.force_miss:        ""
      request_setting.{ident}.force_ssl:         "false"
      request_setting.{ident}.geo_headers:       ""
      request_setting.{ident}.hash_keys:         ""
      request_setting.{ident}.max_stale_age:     ""
      request_setting.{ident}.name:              "request-setting"
      request_setting.{ident}.request_condition: ""
      request_setting.{ident}.timer_support:     ""
      request_setting.{ident}.xff:               "append"
        """.strip()), output) # noqa

    def test_custom_timeouts(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'connect_timeout=12345',
            '-var', 'first_byte_timeout=54321',
            '-var', 'between_bytes_timeout=31337',
            '-target=module.fastly_custom_timeouts',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(template_to_re("""
      backend.{ident}.between_bytes_timeout:     "31337"
      backend.{ident}.connect_timeout:           "12345"
      backend.{ident}.error_threshold:           "0"
      backend.{ident}.first_byte_timeout:        "54321"
        """.strip()), output)

    def test_502_error_condition_page(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'proxy_error_response=<html>error</html>',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert re.search(template_to_re("""
      response_object.{ident}.content:           "<html>error</html>"
        """.strip()), output)

    def test_503_error_condition_page(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'proxy_error_response=<html>error</html>',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert re.search(template_to_re("""
      response_object.{ident}.content:           "<html>error</html>"
        """.strip()), output)

    def test_502_error_condition(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'proxy_error_response=<html>error</html>',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        assert re.search(template_to_re("""
      condition.{ident}.name:                    "response-502-condition"
      condition.{ident}.priority:                "5"
      condition.{ident}.statement:               "beresp.status == 502 && req.http.Cookie:viewerror != \\"true\\""
      condition.{ident}.type:                    "CACHE"
        """.strip()), output) # noqa

        assert re.search(template_to_re("""
      vcl.{ident}.content:                       "964b63eac399fd8aaa928e8e74dc461b7cb0fdc5"
      vcl.{ident}.main:                          "true"
      vcl.{ident}.name:                          "custom_vcl"
        """.strip()), output) # noqa

    def test_503_error_condition(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'proxy_error_response=<html>error</html>',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        assert re.search(template_to_re("""
      condition.{ident}.name:                     "response-503-condition"
      condition.{ident}.priority:                 "5"
      condition.{ident}.statement:                "beresp.status == 503 && req.http.Cookie:viewerror != \\"true\\""
      condition.{ident}.type:                     "CACHE"
        """.strip()), output) # noqa

    def test_ssl_cert_hostname(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'ssl_cert_hostname=test-hostname',
            '-target=module.fastly_ssl_cert_hostname',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        assert re.search(template_to_re("""
     backend.{ident}.ssl_cert_hostname:         "test-hostname"
        """.strip()), output) # noqa

    def test_use_ssl(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'ssl_cert_hostname=test-hostname',
            '-target=module.fastly_ssl_cert_hostname',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        assert re.search(template_to_re("""
     backend.{ident}.use_ssl:                   "true"
        """.strip()), output) # noqa


    def test_custom_vcl_backends_added(self):
        # Given When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'custom_vcl_backends=foo',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(template_to_re("""
      vcl.{ident}.content:                       "cfc34febb4106525e7a97fc683a07e49ac5fc889"
      vcl.{ident}.main:                          "true"
      vcl.{ident}.name:                          "custom_vcl"
        """.strip()), output) # noqa

    def test_custom_vcl_recv_added(self):
        # Given When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'custom_vcl_recv=bar',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(template_to_re("""
      vcl.{ident}.content:                        "651d4c4ceabbd8653d619a6810a2b4c16d5c4591"
      vcl.{ident}.main:                           "true"
      vcl.{ident}.name:                           "custom_vcl"
        """.strip()), output) # noqa

    def test_custom_vcl_error_added(self):
        # Given When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'custom_vcl_error=baz',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(template_to_re("""
      vcl.{ident}.content:                        "7ca7b5134ba45d3f0fb1ac2e93fe817c210ece9e"
      vcl.{ident}.main:                           "true"
      vcl.{ident}.name:                           "custom_vcl"
        """.strip()), output) # noqa

    def test_shield_default(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(r'backend.\d+.shield:\s+""', output)

    def test_shield_set(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'shield=test-shield',
            '-target=module.fastly_set_shield',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert re.search(r'backend.\d+.shield:\s+"test-shield"', output)
