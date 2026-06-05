*** Settings ***
Documentation       ZK proof verification tests.

Resource            ../common.robot

Suite Setup         Set Base URL


*** Test Cases ***
ZK-01 Verify Age Proof
    ${resp}=    Call Api    POST    /v1/zk/verify    data={"proof_system":"noir","proof_b64":"aGVsbG8=","public_inputs":{"min_age":18,"current_ts":1717000000,"dob_ts":0}}    expected_status=200

ZK-02 Verify Rejects Unknown System
    Call Api    POST    /v1/zk/verify    data={"proof_system":"unknown","proof_b64":"aGVsbG8=","public_inputs":{}}    expected_status=400

ZK-03 Verify Income Range
    ${resp}=    Call Api    POST    /v1/zk/verify    data={"proof_system":"risc0","proof_b64":"aGVsbG8=","public_inputs":{"lower_usd":50000,"upper_usd":100000}}    expected_status=200
