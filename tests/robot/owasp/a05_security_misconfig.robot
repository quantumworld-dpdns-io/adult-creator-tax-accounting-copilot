*** Settings ***
Documentation       OWASP Top-10 2021 — A05:2021 Security Misconfiguration.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
A05-01 No Default Credentials
    ${resp}=    Call Api    POST    /oauth2/token    data={"client_id":"admin","client_secret":"admin"}    expected_status=401

A05-02 Security Headers
    ${resp}=    GET    ${BASE_URL}/healthz    expected_status=200
    Dictionary Should Contain Key    ${resp.headers}    X-Content-Type-Options
    Dictionary Should Contain Key    ${resp.headers}    X-Frame-Options
    Dictionary Should Contain Key    ${resp.headers}    Strict-Transport-Security

A05-03 No CORS Misconfig
    ${resp}=    OPTIONS    ${BASE_URL}/v1/creators    headers={"Origin":"https://attacker.example","Access-Control-Request-Method":"GET"}    expected_status=any
    Run Keyword If    "${resp.headers.get('Access-Control-Allow-Origin','')}" == "*"    Fail    CORS too permissive
