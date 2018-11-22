data "aws_secretsmanager_secret" "secret" {
  count = "${var.run_data}"
  name  = "tf_fastly_frontend/${var.env == "live" ? "live" : "aslive"}/fastly-to-datadog-api"
}

data "aws_secretsmanager_secret_version" "secret" {
  count     = "${var.run_data}"
  secret_id = "${data.aws_secretsmanager_secret.secret.id}"
}
