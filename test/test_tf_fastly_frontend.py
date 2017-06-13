import unittest
import os
from subprocess import check_call, check_output

cwd = os.getcwd()


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
            '-var', 'domain_name=domain.com',
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

        assert """
    domain.#:                                     "1"
    domain.1665706793.comment:                    ""
    domain.1665706793.name:                       "ci-www.domain.com"
        """.strip() in output

        assert """
Plan: 1 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_create_fastly_service_in_live_creates_redirection(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
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

        assert """
    domain.#:                                     "1"
    domain.2448670921.comment:                    ""
    domain.2448670921.name:                       "www.domain.com"
        """.strip() in output

        assert """
+ module.fastly.fastly_service_v1.fastly_bare_domain_redirection
        """.strip() in output

        assert """
    header.1405633346.source:                     "\\"https://domain.com\\" + req.url"
        """.strip() in output # noqa

        assert """
Plan: 2 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_create_fastly_service_with_custom_prefix_ci_env(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-var', 'prefix=admin',
            '-target=module.fastly_custom_prefix',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert """
    default_host:                                 "ci-admin.domain.com"
        """.strip() in output

        assert """
    domain.#:                                     "1"
    domain.4266294051.comment:                    ""
    domain.4266294051.name:                       "ci-admin.domain.com"
        """.strip() in output

        assert """
Plan: 1 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_create_fastly_service_with_custom_prefix_live_env(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=live',
            '-var', 'prefix=admin',
            '-target=module.fastly_custom_prefix',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert """
    default_host:                                 "admin.domain.com"
        """.strip() in output

        assert """
    domain.#:                                     "1"
    domain.2052375204.comment:                    ""
    domain.2052375204.name:                       "admin.domain.com"
        """.strip() in output

        assert """
Plan: 2 to add, 0 to change, 0 to destroy.
        """.strip() in output

    def test_delete_x_powered_by_header(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-target=module.fastly',
            '-no-color',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert """
    header.#:                                     "2"
    header.2180504608.action:                     "delete"
    header.2180504608.cache_condition:            ""
    header.2180504608.destination:                "http.X-Powered-By"
    header.2180504608.ignore_if_set:              "false"
    header.2180504608.name:                       "Remove X-Powered-By header"
    header.2180504608.priority:                   "100"
    header.2180504608.regex:                      "<computed>"
    header.2180504608.request_condition:          ""
    header.2180504608.response_condition:         ""
    header.2180504608.source:                     "<computed>"
    header.2180504608.substitution:               "<computed>"
    header.2180504608.type:                       "cache"
        """.strip() in output

    def test_obfuscate_server_header(self):
        # Given

        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # Then
        assert """
    header.3700817666.action:                     "set"
    header.3700817666.cache_condition:            ""
    header.3700817666.destination:                "http.Server"
    header.3700817666.ignore_if_set:              "false"
    header.3700817666.name:                       "Obfuscate Server header"
    header.3700817666.priority:                   "100"
    header.3700817666.regex:                      "<computed>"
    header.3700817666.request_condition:          ""
    header.3700817666.response_condition:         ""
    header.3700817666.source:                     "\\"LHC\\""
    header.3700817666.substitution:               "<computed>"
    header.3700817666.type:                       "cache"
        """.strip() in output

    def test_override_robots_for_non_live_environments(self):
        # given

        # when
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert """
    response_object.#:                            "1"
    response_object.1851546840.cache_condition:   ""
    response_object.1851546840.content:           "User-agent: *\\nDisallow: /\\n"
    response_object.1851546840.content_type:      "text/plain"
    response_object.1851546840.name:              "override-robots.txt"
    response_object.1851546840.request_condition: "override-robots.txt-condition"
    response_object.1851546840.response:          "OK"
    response_object.1851546840.status:            "200"
        """.strip() in output # noqa

        assert """
    condition.#:                                  "2"
    condition.212367000.name:                     "all_urls"
    condition.212367000.priority:                 "10"
    condition.212367000.statement:                "req.url ~ \\".*\\""
    condition.212367000.type:                     "REQUEST"
    condition.820439921.name:                     "override-robots.txt-condition"
    condition.820439921.priority:                 "5"
    condition.820439921.statement:                "req.url ~ \\"^/robots.txt\\""
    condition.820439921.type:                     "REQUEST"
        """.strip() in output # noqa

    def test_force_ssl_and_caching_enabled_by_default(self):
        # given

        # when
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert """
    request_setting.#:                            "1"
    request_setting.4061384956.action:            ""
    request_setting.4061384956.bypass_busy_wait:  ""
    request_setting.4061384956.default_host:      ""
    request_setting.4061384956.force_miss:        "false"
    request_setting.4061384956.force_ssl:         "true"
    request_setting.4061384956.geo_headers:       ""
    request_setting.4061384956.hash_keys:         ""
    request_setting.4061384956.max_stale_age:     "60"
    request_setting.4061384956.name:              "disable caching"
    request_setting.4061384956.request_condition: "all_urls"
    request_setting.4061384956.timer_support:     ""
    request_setting.4061384956.xff:               "append"
        """.strip() in output # noqa

    def test_disable_caching(self):
        # when
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'caching=false',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly_disable_caching',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert """
    request_setting.#:                            "1"
    request_setting.2432135539.action:            ""
    request_setting.2432135539.bypass_busy_wait:  ""
    request_setting.2432135539.default_host:      ""
    request_setting.2432135539.force_miss:        "true"
    request_setting.2432135539.force_ssl:         "true"
    request_setting.2432135539.geo_headers:       ""
    request_setting.2432135539.hash_keys:         ""
    request_setting.2432135539.max_stale_age:     "60"
    request_setting.2432135539.name:              "disable caching"
    request_setting.2432135539.request_condition: "all_urls"
    request_setting.2432135539.timer_support:     ""
    request_setting.2432135539.xff:               "append"
        """.strip() in output # noqa

    def test_disable_force_ssl(self):
        # when
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
            '-var', 'backend_address=1.1.1.1',
            '-var', 'force_ssl=false',
            '-var', 'env=ci',
            '-no-color',
            '-target=module.fastly_disable_force_ssl',
            'test/infra'
        ], env=self._env_for_check_output('qwerty')).decode('utf-8')

        # then
        assert """
    request_setting.#:                            "1"
    request_setting.2559674034.action:            ""
    request_setting.2559674034.bypass_busy_wait:  ""
    request_setting.2559674034.default_host:      ""
    request_setting.2559674034.force_miss:        "false"
    request_setting.2559674034.force_ssl:         "false"
    request_setting.2559674034.geo_headers:       ""
    request_setting.2559674034.hash_keys:         ""
    request_setting.2559674034.max_stale_age:     "60"
    request_setting.2559674034.name:              "disable caching"
    request_setting.2559674034.request_condition: "all_urls"
    request_setting.2559674034.timer_support:     ""
    request_setting.2559674034.xff:               "append"
        """.strip() in output # noqa

    def test_custom_timeouts(self):
        # When
        output = check_output([
            'terraform',
            'plan',
            '-var', 'domain_name=domain.com',
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
        assert """
    backend.4115911643.between_bytes_timeout:     "31337"
    backend.4115911643.connect_timeout:           "12345"
    backend.4115911643.error_threshold:           "0"
    backend.4115911643.first_byte_timeout:        "54321"
        """.strip() in output
