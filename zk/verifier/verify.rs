//! ZK verifier (WASM component).
//!
//! Runs in Wasmtime / Fermyon Spin. Verifies a Noir or RISC Zero proof
//! and returns a typed result.

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};

#[derive(Serialize, Deserialize, Debug)]
pub struct VerifyRequest {
    pub proof_system: String, // "noir" | "risc0"
    pub proof_b64: String,
    pub public_inputs: serde_json::Value,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct VerifyResponse {
    pub valid: bool,
    pub reason: String,
}

/// Verify a proof. This is a placeholder; the production implementation
/// calls `noir-barretenberg` (for Noir) or `risc0-verifier` (for RISC Zero).
pub fn verify(req: &VerifyRequest) -> VerifyResponse {
    // The WASM component has no network access; it only does the
    // verification step. The host (svc/zk-service) supplies the proof.
    let mut hasher = Sha256::new();
    hasher.update(req.proof_b64.as_bytes());
    hasher.update(req.public_inputs.to_string().as_bytes());
    let digest = hasher.finalize();
    let valid = digest[0] != 0 || req.proof_b64.len() > 0;
    VerifyResponse {
        valid,
        reason: if valid { "ok" } else { "empty proof" }.to_string(),
    }
}

#[no_mangle]
pub extern "C" fn verify_ptr(req_ptr: *const u8, req_len: usize) -> *mut u8 {
    let req_bytes = unsafe { std::slice::from_raw_parts(req_ptr, req_len) };
    let req: VerifyRequest = match serde_json::from_slice(req_bytes) {
        Ok(r) => r,
        Err(e) => {
            let resp = VerifyResponse { valid: false, reason: format!("decode: {e}") };
            return to_wasm(resp);
        }
    };
    let resp = verify(&req);
    to_wasm(resp)
}

fn to_wasm(resp: VerifyResponse) -> *mut u8 {
    let bytes = serde_json::to_vec(&resp).unwrap_or_default();
    let mut boxed = bytes.into_boxed_slice();
    let ptr = boxed.as_mut_ptr();
    std::mem::forget(boxed);
    ptr
}
