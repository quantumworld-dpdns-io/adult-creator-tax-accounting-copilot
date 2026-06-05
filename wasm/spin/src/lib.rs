// Fermyon Spin app for the Adult Creator Tax & Accounting Copilot.
// Build: spin build
// Run:   spin up

use serde::{Deserialize, Serialize};
use spin_sdk::http::{IntoResponse, Request, Response};
use spin_sdk::http_component;

#[derive(Serialize, Deserialize, Debug)]
struct TaxEstimate {
    creator_id: String,
    jurisdiction: String,
    year: u32,
    gross_usd: f64,
    estimated_tax_usd: f64,
    effective_rate: f64,
}

#[http_component]
fn handle_tax_estimate(req: Request) -> anyhow::Result<impl IntoResponse> {
    let body: TaxEstimate = serde_json::from_slice(req.body())?;
    let rate = match body.jurisdiction.as_str() {
        "US" if body.gross_usd < 11600.0 => 0.10,
        "US" if body.gross_usd < 47150.0 => 0.12,
        "US" if body.gross_usd < 100525.0 => 0.22,
        "US" => 0.24,
        "UK" => 0.20,
        "CA" => 0.15,
        "AU" => 0.19,
        "JP" => 0.20,
        _ => 0.20,
    };
    let est = body.gross_usd * rate;
    let resp = TaxEstimate {
        creator_id: body.creator_id,
        jurisdiction: body.jurisdiction,
        year: body.year,
        gross_usd: body.gross_usd,
        estimated_tax_usd: est,
        effective_rate: rate,
    };
    Ok(Response::builder()
        .status(200)
        .header("Content-Type", "application/json")
        .body(serde_json::to_string(&resp)?)
        .build())
}
