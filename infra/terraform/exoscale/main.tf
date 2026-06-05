// SKS (Exoscale Kubernetes Service) module
terraform {
  required_providers {
    exoscale = {
      source  = "exoscale/exoscale"
      version = "~> 0.50"
    }
  }
}

variable "name" {}
variable "zone" { default = "ch-gva-2" }
variable "k8s_version" { default = "1.30" }
variable "instance_type" { default = "standard.medium" }
variable "size" { default = 3 }
variable "min_size" { default = 1 }
variable "max_size" { default = 10 }

resource "exoscale_sks_cluster" "this" {
  name          = var.name
  zone          = var.zone
  version       = var.k8s_version
  service_level = "pro"
  cni           = "calico"
}

resource "exoscale_sks_nodepool" "this" {
  cluster_id   = exoscale_sks_cluster.this.id
  zone         = var.zone
  name         = "${var.name}-pool"
  instance_type = var.instance_type
  size         = var.size
  min_size     = var.min_size
  max_size     = var.max_size
  anti_affinity_group_ids = []
}

output "cluster_id" { value = exoscale_sks_cluster.this.id }
output "endpoint"   { value = exoscale_sks_cluster.this.endpoint }
