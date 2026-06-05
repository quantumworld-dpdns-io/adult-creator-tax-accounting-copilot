// Pulumi program: Scaleway (EU)
//
// Provisions: K8s cluster (Kapsule), managed Postgres, Redis, Object Storage.

import * as pulumi from "@pulumi/pulumi";
import * as scaleway from "@pulumi/scaleway";

const stack = pulumi.getStack();
const cfg = new pulumi.Config();

const cluster = new scaleway.K8sCluster(`${stack}-k8s`, {
  version: "1.30",
  cni: "cilium",
  region: "eu-west",
});

const nodePool = new scaleway.K8sPool(`${stack}-pool-general`, {
  clusterId: cluster.id,
  nodeType: "GP1-S",
  size: 3,
  minSize: 1,
  maxSize: 10,
  autoscaling: true,
  containerRuntime: "containerd",
});

const gpuPool = new scaleway.K8sPool(`${stack}-pool-gpu`, {
  clusterId: cluster.id,
  nodeType: "H100-1-80",
  size: 0,
  minSize: 0,
  maxSize: 4,
  autoscaling: true,
});

const db = new scaleway.RdbInstance(`${stack}-postgres`, {
  engine: "PostgreSQL-16",
  nodeType: "DB-DEV-S",
  isHaCluster: false,
  region: "eu-west",
});

const redis = new scaleway.RedisCluster(`${stack}-redis`, {
  version: "7.2",
  nodeType: "RED1-XS",
  replicas: 1,
  region: "eu-west",
});

const bucket = new scaleway.ObjectBucket(`${stack}-copilot-data`, {
  region: "eu-west",
});

export const clusterId = cluster.id;
export const kubeconfig = cluster.kubeconfigs[0].configFile;
export const dbEndpoint = db.endpoint;
export const redisEndpoint = redis.endpoints[0];
export const bucketName = bucket.name;
