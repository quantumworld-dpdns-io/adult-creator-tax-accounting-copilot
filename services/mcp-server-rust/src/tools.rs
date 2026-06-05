//! Tool dispatch stub.

use serde_json::{json, Value};

pub fn dispatch(req: &Value) -> Value {
    let method = req.get("method").and_then(|v| v.as_str()).unwrap_or("");
    match method {
        "initialize" => json!({
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": { "name": "adult-creator-tax-copilot", "version": "0.1.0" },
                "capabilities": { "tools": {} }
            }
        }),
        "tools/list" => json!({
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "result": {
                "tools": [
                    { "name": "get_payouts",        "description": "Fetch aggregated payouts" },
                    { "name": "compute_tax_estimate","description": "Compute tax estimate" },
                    { "name": "file_1099",          "description": "Generate 1099 form" },
                    { "name": "verify_age_zk",      "description": "ZK age proof" },
                ]
            }
        }),
        "tools/call" => {
            let name = req.pointer("/params/name").and_then(|v| v.as_str()).unwrap_or("");
            let args = req.pointer("/params/arguments").cloned().unwrap_or(json!({}));
            let result = match name {
                "get_payouts" => json!({
                    "currency": "USD",
                    "gross": 12345.67, "fees": 234.56, "net": 12111.11,
                    "args": args
                }),
                "compute_tax_estimate" => json!({
                    "estimated_tax_usd": 2456.78, "effective_rate": 0.21, "args": args
                }),
                "file_1099" => json!({
                    "pdf_url": format!("s3://copilot-data/1099/{}/{}.pdf",
                        args.get("creator_id").and_then(|v| v.as_str()).unwrap_or("unknown"),
                        args.get("year").and_then(|v| v.as_i64()).unwrap_or(0)),
                    "signed": true,
                    "signature_algo": "Dilithium-5",
                    "args": args
                }),
                "verify_age_zk" => json!({
                    "proof_system": "noir", "curve": "bn254",
                    "args": args
                }),
                _ => json!({ "error": format!("unknown tool: {name}") })
            };
            json!({
                "jsonrpc": "2.0",
                "id": req.get("id"),
                "result": { "content": [{ "type": "text", "text": result.to_string() }] }
            })
        }
        _ => json!({
            "jsonrpc": "2.0",
            "id": req.get("id"),
            "error": { "code": -32601, "message": "method not found" }
        }),
    }
}
