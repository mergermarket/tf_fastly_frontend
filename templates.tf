data "template_file" "robotstxt" {
  template = <<EOF
User-agent: *
Disallow: /
EOF
}
