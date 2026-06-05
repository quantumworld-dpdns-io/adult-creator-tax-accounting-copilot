// Scaleway Kapsule (K8s) module
terraform {
  required_providers {
    scaleway = { source = "scaleway/scaleway", version = "~> 2.50" }
  }
}

variable "name" {}
variable "region" { default = "eu-west" }
variable "k8s_version" { default = "1.30" }

resource "scaleway_k8s_cluster" "this" {
  name    = var.name
  version = var.k8s_version
  cni     = "cilium"
  region  = var.region
}

resource "scaleway_k8s_pool" "general" {
  cluster_id  = scaleway_k8s_cluster.this.id
  name        = "${var.name}-general"
  node_type   = "GP1-S"
  size        = 3
  min_size    = 1
  max_size    = 10
  autoscaling = true
  region      = var.region
}

resource "scaleway_k8s_pool" "gpu" {
  cluster_id  = scaleway_k8s_cluster.this.id
  name        = "${var.name}-gpu"
  node_type   = "H100-1-80"
  size        = 0
  min_size    = 0
  max_size    = 4
  autoscaling = true
  region      = var.region
}

resource "scaleway_rdb_instance" "postgres" {
  name           = "${var.name}-pg"
  engine         = "PostgreSQL-16"
  node_type      = "DB-DEV-S"
  is_ha_cluster  = false
  region         = var.region
}

resource "scaleway_redis_cluster" "redis" {
  name      = "${var.name}-redis"
  version   = "7.2"
  node_type = "RED1-XS"
  replicas  = 1
  region    = var.region
}

output "cluster_id"     { value = scaleway_k8s_cluster.this.id }
output "kubeconfig"     { value = scaleway_k8s_cluster.this.kubeconfig[0].config_file }
output "postgres_host"  { value = scaleway_rdb_instance.postgres.endpoint }
output "redis_host"     { value = scaleway_redis_cluster.redis.endpoints[0] }
