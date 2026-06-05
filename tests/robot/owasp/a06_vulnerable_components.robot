*** Settings ***
Documentation       OWASP Top-10 2021 — A06:2021 Vulnerable & Outdated Components.
...                 Verifies that the SBOM is present, no critical CVEs are open,
...                 and OS packages are up to date.

Resource            ../common.robot


*** Test Cases ***
A06-01 SBOM Exists
    File Should Exist    ${CURDIR}/../../sbom/syft.spdx.json

A06-02 No Critical CVEs
    ${output}=    Run Process    grype    dir:.    --fail-on    critical
    ...    timeout=120s    stderr=STDOUT
    Should Be Equal As Integers    ${output.rc}    0

A06-03 OS Patches Up To Date
    ${output}=    Run Process    apt    list    --upgradable
    ...    timeout=30s    stderr=STDOUT
    Should Not Contain    ${output.stdout}    libssl
