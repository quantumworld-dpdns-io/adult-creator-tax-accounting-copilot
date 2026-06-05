*** Settings ***
Documentation       Quantum simulator tests via the API.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
Q-01 Qrng Bits Endpoint
    ${resp}=    GET    ${BASE_URL}/v1/qrng/bits?provider=sim&bits=128    expected_status=200
    Length Should Be    ${resp.json()['hex']}    32

Q-02 Qrng Rejects Invalid Provider
    GET    ${BASE_URL}/v1/qrng/bits?provider=bogus&bits=128    expected_status=422

Q-03 Qrng Rejects Excessive Bits
    GET    ${BASE_URL}/v1/qrng/bits?provider=sim&bits=99999    expected_status=422

Q-04 Qrng Bits Are Unique
    ${a}=    GET    ${BASE_URL}/v1/qrng/bits?provider=sim&bits=128    expected_status=200
    ${b}=    GET    ${BASE_URL}/v1/qrng/bits?provider=sim&bits=128    expected_status=200
    Should Not Be Equal    ${a.json()['hex']}    ${b.json()['hex']}
