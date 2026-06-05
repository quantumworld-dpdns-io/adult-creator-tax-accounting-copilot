// Zeabur module — uses the Zeabur API via null_resource + curl.
terraform {
  required_providers {
    http = { source = "hashicorp/http", version = "~> 3.4" }
  }
}

variable "zeabur_token" { sensitive = true }
variable "project_name" {}
variable "region" { default = "tw-1" }

locals {
  services = [
    "api-gateway", "tax-engine", "ledger", "payout-aggregator",
    "crypto-tax", "realtime-pricing", "mcp-server"
  ]
}

resource "null_resource" "project" {
  triggers = { project = var.project_name }
  provisioner "local-exec" {
    command = <<-EOT
      set -euo pipefail
      curl -fsSL -X POST https://api.zeabur.com/v1/projects \
        -H "Authorization: Bearer ${var.zeabur_token}" \
        -H "Content-Type: application/json" \
        -d '{"name":"${var.project_name}","region":"${var.region}"}'
    EOT
  }
}

output "project_name" { value = var.project_name }
