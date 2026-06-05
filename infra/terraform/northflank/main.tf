terraform {
  required_providers {
    northflank = { source = "northflank/northflank", version = "~> 0.4" }
  }
}

variable "northflank_token" { sensitive = true }
variable "project_name" {}
variable "region" { default = "eu-west-1" }

resource "northflank_project" "this" {
  name   = var.project_name
  region = var.region
}

resource "northflank_addon" "postgres" {
  project_id = northflank_project.this.id
  type       = "postgres"
  version    = "16"
  name       = "${var.project_name}-postgres"
}

resource "northflank_addon" "redis" {
  project_id = northflank_project.this.id
  type       = "redis"
  version    = "7"
  name       = "${var.project_name}-redis"
}

output "project_id" { value = northflank_project.this.id }
