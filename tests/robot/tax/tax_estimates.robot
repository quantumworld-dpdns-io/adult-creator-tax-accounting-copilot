*** Settings ***
Documentation       Robot Framework tests for the tax-engine.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
Tax-01 US Low Bracket 10%
    ${resp}=    Call Api    POST    /v1/tax/estimate    data={"creator_id":"alice","jurisdiction":"US","year":2026,"payouts":[{"platform":"OnlyFans","currency":"USD","gross":5000,"fees":100,"net":4900}]}
    Should Be Equal As Numbers    ${resp.json()['effective_rate']}    0.10
    Should Be Equal As Strings    ${resp.json()['bracket']}    10%

Tax-02 US 22% Bracket
    ${resp}=    Call Api    POST    /v1/tax/estimate    data={"creator_id":"alice","jurisdiction":"US","year":2026,"payouts":[{"platform":"OnlyFans","currency":"USD","gross":60000,"fees":1200,"net":58800}]}
    Should Be Equal As Strings    ${resp.json()['bracket']}    22%

Tax-03 UK Basic Rate
    ${resp}=    Call Api    POST    /v1/tax/estimate    data={"creator_id":"bob","jurisdiction":"UK","year":2026,"payouts":[]}
    Should Be Equal As Strings    ${resp.json()['bracket']}    basic-rate

Tax-04 File 1099-NEC
    ${resp}=    Call Api    POST    /v1/tax/file/1099    data={"creator_id":"alice","year":2026,"form":"1099-NEC"}    expected_status=200
    Should Be True    ${resp.json()['signed']}

Tax-05 File W-8BEN
    ${resp}=    Call Api    POST    /v1/tax/file/w8ben    data={"creator_id":"alice","treaty_country":"DE"}    expected_status=200

Tax-06 VAT MOSS Aggregation
    ${resp}=    Call Api    POST    /v1/tax/aggregate/vat    data={"creator_id":"alice","period":"2026-Q1"}    expected_status=200
    Should Be True    ${resp.json()['total_vat_collected']} > 0
