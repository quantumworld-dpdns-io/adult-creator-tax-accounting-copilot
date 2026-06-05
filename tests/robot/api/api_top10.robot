*** Settings ***
Documentation       OWASP API Security Top-10 — subset.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
API1-01 BOLA On 1099 Endpoint
    ${resp}=    Call Api    GET    /v1/creators/bob/1099    expected_status=403

API2-01 Broken Authentication
    Create Session    attacker    ${BASE_URL}
    GET    ${BASE_URL}/v1/creators/alice/payouts    expected_status=401

API3-01 BOPLA On Tax Estimate
    [Documentation]    Excess properties must be rejected.
    ${resp}=    Call Api    POST    /v1/creators/alice/tax-estimate    data={"jurisdiction":"US","year":2026,"extra":"foo"}    expected_status=400

API4-01 Resource Consumption
    [Documentation]    Pagination limit enforced.
    ${resp}=    Call Api    GET    /v1/creators/alice/payouts?start=2025-01-01&end=2025-12-31&limit=99999    expected_status=400

API5-01 BFLA On Admin
    ${resp}=    Call Api    POST    /v1/admin/users    data={"role":"admin"}    expected_status=403

API6-01 SSRF
    ${resp}=    Call Api    POST    /v1/creators/alice/avatar/fetch    data={"url":"http://localhost:5432/"}    expected_status=400

API7-01 Security Misconfig
    ${resp}=    GET    ${BASE_URL}/v1/internal/config    expected_status=404

API8-01 Lack Of Protection From Automated Threats
    [Documentation]    Bot-defense in place (Turnstile / hCaptcha).
    ${resp}=    Call Api    POST    /v1/creators    data={"name":"alice"}    expected_status=any
    Dictionary Should Contain Key    ${resp.headers}    X-Bot-Defense

API9-01 Improper Asset Management
    [Documentation]    No /v0/, /debug, /swagger.json.
    GET    ${BASE_URL}/v0/creators    expected_status=404
    GET    ${BASE_URL}/debug    expected_status=404
    GET    ${BASE_URL}/swagger.json    expected_status=404

API10-01 Unsafe Consumption Of APIs
    [Documentation]    A webhook from a disallowed host is rejected.
    ${resp}=    POST    ${BASE_URL}/v1/webhooks/incoming    data=${EMPTY}    headers={"X-Source":"attacker.example"}    expected_status=400
