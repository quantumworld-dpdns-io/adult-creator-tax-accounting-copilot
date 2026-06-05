*** Settings ***
Documentation       OWASP Top-10 2021 — A08:2021 Software & Data Integrity Failures.

Resource            ../common.robot


*** Test Cases ***
A08-01 Signed Container Image
    [Documentation]    Image must have a cosign signature.
    ${output}=    Run Process    cosign    verify    --certificate-identity-regexp    .*    --certificate-oidc-issuer    https://token.actions.githubusercontent.com    ghcr.io/quantumworld-dpdns-io/api-gateway:latest
    ...    timeout=60s    stderr=STDOUT
    Should Be Equal As Integers    ${output.rc}    0

A08-02 SLSA Provenance Present
    File Should Exist    ${CURDIR}/../../provenance/api-gateway.intoto.jsonl

A08-03 SBOM Integrity
    [Documentation]    SBOM must be signed or attached to the release.
    File Should Exist    ${CURDIR}/../../sbom/syft.spdx.json
    ${output}=    Run Process    cosign    verify-attestation    --type    spdxjson    ghcr.io/quantumworld-dpdns-io/api-gateway:latest
    ...    timeout=60s    stderr=STDOUT
    Should Be Equal As Integers    ${output.rc}    0
