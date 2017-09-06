data "logentries_logset" "fastly" {
  name = "${var.le_logset_parent_name}"
}

resource "logentries_log" "logs" {
  logset_id = "${data.logentries_logset.fastly.id}"
  name      = "${var.env}-${var.domain_name}"
  source    = "token"
}
