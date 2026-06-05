*** Settings ***
Documentation       Payment-platform webhook tests.

Resource            ../common.robot

Suite Setup         Set Base Base URL
Suite Setup         Set Base URL


*** Keywords ***
Set Base Base URL
    Set Suite Variable    \${BASE_URL}    http://localhost:8080


*** Test Cases ***
Pay-01 OnlyFans Webhook
    ${resp}=    POST    ${BASE_URL}/v1/webhooks/onlyfans    data=${EMPTY}    headers={"X-Of-Signature":"abc","Content-Type":"application/json"}    expected_status=any
    Should Be True    ${resp.status_code} in [200, 202, 401]

Pay-02 Fansly Webhook
    POST    ${BASE_URL}/v1/webhooks/fansly    data=${EMPTY}    headers={"X-Fansly-Signature":"abc"}    expected_status=any

Pay-03 Stripe Webhook
    POST    ${BASE_URL}/v1/webhooks/stripe    data=${EMPTY}    headers={"Stripe-Signature":"t=,v1=abc"}    expected_status=any

Pay-04 Coinbase Commerce Webhook
    POST    ${BASE_URL}/v1/webhooks/coinbase-commerce    data=${EMPTY}    headers={"X-CC-Webhook-Signature":"abc"}    expected_status=any
