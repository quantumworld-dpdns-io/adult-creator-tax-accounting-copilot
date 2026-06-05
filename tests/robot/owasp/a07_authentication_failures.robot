*** Settings ***
Documentation       OWASP Top-10 2021 — A07:2021 Identification & Authentication Failures.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
A07-01 Credential Stuffing Blocked
    FOR    ${pw}    IN    password    123456    qwerty
        Call Api    POST    /oauth2/token    data={"client_id":"alice","client_secret":"${pw}"}    expected_status=401
    END

A07-02 MFA Required For Sensitive Flows
    ${resp}=    Call Api    POST    /v1/creators/alice/withdraw    data=${EMPTY}    expected_status=401

A07-03 Session Fixation Prevented
    ${s1}=    GET    ${BASE_URL}/v1/session    expected_status=any
    ${s2}=    GET    ${BASE_URL}/v1/session    expected_status=any
    Run Keyword If    "${s1.headers.get('Set-Cookie','')}" == "${s2.headers.get('Set-Cookie','')}"    Fail    Same cookie reused
