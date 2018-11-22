output "datadog_api_key" {
  value = "${element(concat(data.aws_secretsmanager_secret_version.secret.*.secret_string, list("")), 0)}"
}
