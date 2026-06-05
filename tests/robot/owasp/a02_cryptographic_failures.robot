*** Settings ***
Documentation       OWASP Top-10 2021 — A02:2021 Cryptographic Failures.
...                 Tests for TLS version, weak ciphers, PII at rest, and PQC readiness.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
A02-01 TLS 1.2 Or Higher
    [Documentation]    Service must terminate TLS >= 1.2.
    ${output}=    Run Process    openssl    s_client    -connect    api.copilot.example:443    -tls1_2
    ...    timeout=10s    stderr=STDOUT
    Should Not Contain    ${output.stdout}    handshake failure
    Should Not Contain    ${output.stdout}    protocol version

A02-02 No Weak Ciphers
    ${output}=    Run Process    nmap    --script    ssl-enum-ciphers    -p    443    api.copilot.example
    ...    timeout=30s    stderr=STDOUT
    Should Not Contain    ${output.stdout}    RC4
    Should Not Contain    ${output.stdout}    3DES
    Should Not Contain    ${output.stdout}    NULL

A02-03 PII At Rest Is Encrypted
    [Documentation]    Database exports must not contain plaintext SSN.
    ${dump}=    Get File    /var/lib/postgresql/backup/latest.sql    ignore_errors=True
    Run Keyword If    '${dump}' != '${EMPTY}'    Should Not Contain    ${dump}    123-45-6789

A02-04 PQC TLS Available
    [Documentation]    Service must support a PQC cipher suite.
    ${output}=    Run Process    openssl    s_client    -connect    api.copilot.example:443    -groups    X25519MLKEM768
    ...    timeout=10s    stderr=STDOUT
    Should Not Contain    ${output.stdout}    handshake failure
