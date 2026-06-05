*** Settings ***
Documentation       Robot Framework suite for the Adult Creator Tax & Accounting Copilot.
...                 This root suite imports all sub-suites (OWASP, API, quantum, ZK, tax, payments).

Suite Setup         Setup Suite
Suite Teardown      Teardown Suite

Library             Collections
Library             OperatingSystem
Library             String
Library             DateTime

Resource            common.robot


*** Keywords ***
Setup Suite
    ${ENV}=    Get Variable Value    ${ENV}    dev
    Set Suite Variable    \${ENV}
    Log To Console    Running in environment: ${ENV}

Teardown Suite
    Log To Console    Suite finished.
