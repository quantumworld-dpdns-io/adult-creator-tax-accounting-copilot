*** Settings ***
Documentation       OWASP Top-10 2021 — A04:2021 Insecure Design.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
A04-01 Rate Limit Cannot Be Bypassed
    [Documentation]    A burst of 1000 requests must be rate-limited.
    FOR    ${i}    IN RANGE    0    1000
        Call Api    GET    /v1/creators/alice/payouts?start=2025-01-01&end=2025-12-31    expected_status=any
    END
    ${resp}=    Call Api    GET    /v1/creators/alice/payouts?start=2025-01-01&end=2025-12-31    expected_status=429

A04-02 Workflow Ordering Cannot Be Skipped
    [Documentation]    Cannot file 1099 before KYC.
    ${resp}=    Call Api    POST    /v1/creators/bob/1099    data=${EMPTY}    expected_status=412
