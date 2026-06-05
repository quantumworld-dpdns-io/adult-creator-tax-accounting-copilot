//! Federated learning client (Rust + tonic).
//! This is a minimal scaffold for an FL client that trains a small
//! LoRA adapter on-device and reports gradients to the superlink.

#![allow(dead_code)]

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Gradients {
    pub creator_id: String,
    pub round: u64,
    pub model_version: String,
    pub grads: Vec<f32>,
    pub dp_epsilon: f64,
    pub dp_delta: f64,
    pub sigma: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Round {
    pub round: u64,
    pub global_model_version: String,
    pub clients: u32,
}

pub fn add_dp_noise(grads: &[f32], sigma: f64) -> Vec<f32> {
    // LCG-based gaussian-ish; in production use `rand_distr::Normal`.
    let mut state: u64 = 0x9E3779B97F4A7C15;
    let mut out = Vec::with_capacity(grads.len());
    for &g in grads {
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        let u1 = (state >> 11) as f32 / (1u32 << 21) as f32;
        state = state.wrapping_mul(6364136223846793005).wrapping_add(1442695040888963407);
        let u2 = (state >> 11) as f32 / (1u32 << 21) as f32;
        let gauss = ((-2.0 * u1.max(1e-9) as f64).ln()).sqrt() * (2.0 * 3.14159265 * u2 as f64).cos();
        out.push(g + (gauss * sigma) as f32);
    }
    out
}

pub fn gradients_to_bytes(g: &Gradients) -> Vec<u8> {
    serde_json::to_vec(g).unwrap_or_default()
}
