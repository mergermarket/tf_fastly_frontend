resource "logentries_log" "logs" {
  logset_id = "${var.le_logset_id}"
  name      = "${var.env}-${var.domain_name}"
  source    = "token"
}
