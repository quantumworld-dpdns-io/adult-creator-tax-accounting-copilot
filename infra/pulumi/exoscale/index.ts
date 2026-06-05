// Pulumi program: Exoscale (CH)
//
// Sovereign cloud, GDPR-aligned, FINMA-friendly.

import * as pulumi from "@pulumi/pulumi";
import * as exoscale from "@pulumi/exoscale";

const stack = pulumi.getStack();

const cluster = new exoscale.SksCluster(`${stack}-sks`, {
  zone: "ch-gva-2",
  version: "1.30",
  cni: "calico",
  serviceLevel: "pro",
});

const nodepool = new exoscale.SksNodepool(`${stack}-pool`, {
  clusterId: cluster.id,
  zone: "ch-gva-2",
  instanceType: "standard.medium",
  size: 3,
  minSize: 1,
  maxSize: 10,
});

const db = new exoscale.DbaasPg(`${stack}-postgres`, {
  zone: "ch-gva-2",
  plan: "starter",
  version: "16",
});

const redis = new exoscale.DbaasRedis(`${stack}-redis`, {
  zone: "ch-gva-2",
  plan: "starter",
});

const bucket = new exoscale.SosBucket(`${stack}-copilot`, {
  zone: "ch-gva-2",
});

export const clusterId = cluster.id;
export const endpoint = cluster.endpoint;
export const bucketName = bucket.name;
