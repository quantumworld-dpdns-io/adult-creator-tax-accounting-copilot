*** Settings ***
Documentation       OWASP Top-10 2021 — A10:2021 Server-Side Request Forgery.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
A10-01 SSRF To Cloud Metadata
    [Documentation]    Cannot fetch the AWS metadata endpoint via a webhook URL.
    ${resp}=    Call Api    POST    /v1/creators/alice/webhooks    data={"url":"http://169.254.169.254/latest/meta-data/iam/security-credentials/"}    expected_status=400

A10-02 SSRF To Internal Services
    ${resp}=    Call Api    POST    /v1/creators/alice/webhooks    data={"url":"http://10.0.0.1:5432/"}    expected_status=400

A10-03 DNS Rebinding Mitigation
    [Documentation]    A URL that resolves to a private IP must be blocked.
    ${resp}=    Call Api    POST    /v1/creators/alice/webhooks    data={"url":"http://attacker-controlled.example.com:8080/"}    expected_status=400
