data "aws_secretsmanager_secret" "secret"{
  name = "tf_fastly_frontend/aslive/fastly-to-datadog-api"
}

data "aws_secretsmanager_secret_version" "secret" {
  secret_id = "${data.aws_secretsmanager_secret.secret.id}"
}

output "secret" {
    value = "${data.aws_secretsmanager_secret_version.secret.secret_string}"
}
