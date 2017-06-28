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
        assert """
    default_host:                                 "ci-www.domain.com"
        """.strip() in output

        assert re.search(template_to_re("""
    domain.#:                                     "1"
    domain.{ident}.comment:                    ""
    domain.{ident}.name:                       "ci-www.domain.com"
        """.strip()), output)

        assert """
Plan: 1 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_create_fastly_service_in_live_creates_redirection(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'bare_redirect_domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=live',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert """
+ module.fastly.fastly_service_v1.fastly
        """.strip() in output

        assert """
    default_host:                                 "www.domain.com"
        """.strip() in output

        assert re.search(template_to_re("""
    domain.#:                                     "1"
    domain.{ident}.comment:                    ""
    domain.{ident}.name:                       "www.domain.com"
        """.strip()), output)

        assert """
+ module.fastly.fastly_service_v1.fastly_bare_domain_redirection
        """.strip() in output

        assert re.search(template_to_re("""
    header.{ident}.source:                     "\\"https://www.domain.com\\" + req.url"
        """.strip()), output) # noqa

        assert """
Plan: 2 to add, 0 to change, 0 to destroy.
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
    header.{ident}.regex:                      "<computed>"
    header.{ident}.request_condition:          ""
    header.{ident}.response_condition:         ""
    header.{ident}.source:                     "<computed>"
    header.{ident}.substitution:               "<computed>"
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
    header.{ident}.regex:                      "<computed>"
    header.{ident}.request_condition:          ""
    header.{ident}.response_condition:         ""
    header.{ident}.source:                     "\\"LHC\\""
    header.{ident}.substitution:               "<computed>"
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

    def test_force_ssl_and_caching_enabled_by_default(self):
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
    request_setting.{ident}.bypass_busy_wait:  ""
    request_setting.{ident}.default_host:      ""
    request_setting.{ident}.force_miss:        "false"
    request_setting.{ident}.force_ssl:         "true"
    request_setting.{ident}.geo_headers:       ""
    request_setting.{ident}.hash_keys:         ""
    request_setting.{ident}.max_stale_age:     "60"
    request_setting.{ident}.name:              "disable caching"
    request_setting.{ident}.request_condition: "all_urls"
    request_setting.{ident}.timer_support:     ""
    request_setting.{ident}.xff:               "append"
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
    request_setting.#:                            "1"
    request_setting.{ident}.action:            ""
    request_setting.{ident}.bypass_busy_wait:  ""
    request_setting.{ident}.default_host:      ""
    request_setting.{ident}.force_miss:        "true"
    request_setting.{ident}.force_ssl:         "true"
    request_setting.{ident}.geo_headers:       ""
    request_setting.{ident}.hash_keys:         ""
    request_setting.{ident}.max_stale_age:     "60"
    request_setting.{ident}.name:              "disable caching"
    request_setting.{ident}.request_condition: "all_urls"
    request_setting.{ident}.timer_support:     ""
    request_setting.{ident}.xff:               "append"
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
    request_setting.{ident}.bypass_busy_wait:  ""
    request_setting.{ident}.default_host:      ""
    request_setting.{ident}.force_miss:        "false"
    request_setting.{ident}.force_ssl:         "false"
    request_setting.{ident}.geo_headers:       ""
    request_setting.{ident}.hash_keys:         ""
    request_setting.{ident}.max_stale_age:     "60"
    request_setting.{ident}.name:              "disable caching"
    request_setting.{ident}.request_condition: "all_urls"
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
            '-var', 'error_response_502=<html>502</html>',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert re.search(template_to_re("""
    response_object.{ident}.content:           "<html>502</html>"
        """.strip()), output)

    def test_503_error_condition_page(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'error_response_503=<html>503</html>',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert re.search(template_to_re("""
    response_object.{ident}.content:           "<html>503</html>"
        """.strip()), output)

    def test_502_error_condition(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=www.domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'error_response_502=<html>502</html>',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        assert re.search(template_to_re("""
    condition.{ident1}.type:                    "CACHE"
    condition.{ident2}.name:                    "response-502-condition"
    condition.{ident2}.priority:                "5"
    condition.{ident2}.statement:               "beresp.status == 502"
        """.strip()), output) # noqa
