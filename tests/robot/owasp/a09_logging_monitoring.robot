*** Settings ***
Documentation       OWASP Top-10 2021 — A09:2021 Security Logging & Monitoring Failures.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
A09-01 Failed Login Is Logged
    Call Api    POST    /oauth2/token    data={"client_id":"alice","client_secret":"wrong"}    expected_status=401
    Sleep    2s
    ${resp}=    Call Api    GET    /v1/admin/audit-log?since=now-1m    expected_status=200
    Should Contain    ${resp.text}    invalid_credentials

A09-02 Log Injection Prevented
    ${resp}=    Call Api    POST    /v1/creators    data={"name":"alice\nFAKE LOG ENTRY"}    expected_status=400
    ${resp2}=    Call Api    GET    /v1/admin/audit-log?since=now-1m    expected_status=200
    Should Not Contain    ${resp2.text}    FAKE LOG ENTRY
