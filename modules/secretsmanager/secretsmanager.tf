data "aws_secretsmanager_secret" "secret"{
    count = "${var.run_data}"
    name = "tf_fastly_frontend/aslive/fastly-to-datadog-api"
}

data "aws_secretsmanager_secret_version" "secret" {
    count     = "${var.run_data}"
    secret_id = "${data.aws_secretsmanager_secret.secret.id}"
}

output "datadog_api_key" {
    //value = "${false ? data.aws_secretsmanager_secret_version.secret.*.secret_string : "123456"}"
    value = "${element(concat(data.aws_secretsmanager_secret_version.secret.*.secret_string, list("")), 0)}"
}

variable "run_data" {
    description = "Used to switch off data resources when unit testing"
    default     = true
}
