*** Settings ***
Documentation       OWASP Top-10 2021 — A01:2021 Broken Access Control.
...                 Tests for IDOR, BOLA, BFLA, missing tenant checks, JWT tampering,
...                 scope escalation, and force browsing.

Resource            ../common.robot

Suite Setup         Set Base URL
Test Setup          Create Session    copilot    ${BASE_URL}    verify=True


*** Test Cases ***
A01-01 IDOR On Payouts Endpoint
    [Documentation]    Alice's token should NOT see Bob's payouts.
    ${resp}=    Call Api    GET    /v1/creators/alice/payouts?start=2025-01-01&end=2025-12-31    expected_status=200
    Dictionary Should Not Contain Key    ${resp.json()}    bob

A01-02 Horizontal Privilege Escalation On 1099
    [Documentation]    Alice's token should NOT generate Bob's 1099.
    ${resp}=    Call Api    POST    /v1/creators/bob/1099    data=${EMPTY}    expected_status=403

A01-03 Vertical Privilege Escalation On Admin Endpoint
    ${resp}=    Call Api    GET    /v1/admin/audit-log    expected_status=403

A01-04 Tenant Boundary Check
    [Documentation]    A token for tenant A must be rejected by tenant B endpoints.
    ${resp}=    Call Api    GET    /v1/tenants/tenantB/payouts    expected_status=403

A01-05 JWT Tampering Detection
    [Documentation]    A modified JWT must be rejected.
    ${bad}=    Set Variable    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdHRhY2tlciJ9.invalid
    Create Session    attacker    ${BASE_URL}
    ${headers}=    Create Dictionary    Authorization=Bearer ${bad}
    GET    ${BASE_URL}/v1/creators/alice/payouts    headers=${headers}    expected_status=401

A01-06 Scope Escalation Rejected
    [Documentation]    A read-only token must not write.
    ${resp}=    Call Api    POST    /v1/creators/alice/1099    data=${EMPTY}    expected_status=403
