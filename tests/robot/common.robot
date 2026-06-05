*** Settings ***
Documentation       Common resources for the Adult Creator Tax & Accounting Copilot tests.
...                 Provides the API base URL, OAuth2 token fetching, and helper
...                 keywords shared by all suites.

Library             Collections
Library             OperatingSystem
Library             String
Library             RequestsLibrary


*** Variables ***
${BASE_URL}         ${EMPTY}
${TOKEN}            ${EMPTY}
${ENV}              dev


*** Keywords ***
Set Base URL
    [Documentation]    Pick the base URL for the chosen environment.
    ${base}=    Run Keyword If    '${ENV}' == 'prod'    Set Variable    https://api.copilot.example
    ...         ELSE IF    '${ENV}' == 'staging'    Set Variable    https://staging.copilot.example
    ...         ELSE    Set Variable    http://localhost:8080
    Set Suite Variable    \${BASE_URL}    ${base}

Get Auth Token
    [Documentation]    Fetch a developer OAuth2 token from the local idp.
    ${resp}=    POST    ${BASE_URL}/oauth2/token
    ...    json=${True}    json=${EMPTY}    expected_status=any
    Run Keyword And Ignore Error    Create Session    copilot    ${BASE_URL}    verify=True

Call Api
    [Documentation]    Issue an authenticated HTTP call.
    [Arguments]    ${method}    ${path}    ${data}=${None}    ${expected_status}=200
    ${headers}=    Create Dictionary    Authorization=Bearer ${TOKEN}    Content-Type=application/json
    ${resp}=    Run Keyword If    "${method}" == "GET"
    ...    GET    ${BASE_URL}${path}    headers=${headers}    expected_status=${expected_status}
    ...    ELSE IF    "${method}" == "POST"
    ...    POST    ${BASE_URL}${path}    json=${data}    headers=${headers}    expected_status=${expected_status}
    ...    ELSE IF    "${method}" == "DELETE"
    ...    DELETE    ${BASE_URL}${path}    headers=${headers}    expected_status=${expected_status}
    ...    ELSE    Fail    Unsupported method ${method}
    RETURN    ${resp}

Assert No PII
    [Documentation]    Verify the response body does not contain obvious PII patterns.
    [Arguments]    ${body}    @{patterns}
    FOR    ${p}    IN    @{patterns}
        Should Not Contain    ${body}    ${p}    msg=Response contains PII: ${p}
    END
