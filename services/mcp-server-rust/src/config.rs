//! Settings loaded from env vars.

use serde::Deserialize;
use std::env;

#[derive(Debug, Clone, Deserialize)]
pub struct Settings {
    pub transport: String,
    pub host: String,
    pub port: u16,
    pub log_level: String,
}

impl Settings {
    pub fn from_env() -> anyhow::Result<Self> {
        Ok(Self {
            transport: env::var("MCP_TRANSPORT").unwrap_or_else(|_| "stdio".into()),
            host: env::var("MCP_HOST").unwrap_or_else(|_| "0.0.0.0".into()),
            port: env::var("MCP_PORT").ok().and_then(|v| v.parse().ok()).unwrap_or(8000),
            log_level: env::var("RUST_LOG").unwrap_or_else(|_| "info".into()),
        })
    }
}
