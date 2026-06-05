//! Real-time pricing service (Rust) — fanout quotes over WebSocket.
//! Uses tokio for high-concurrency price ingest.

use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;

use anyhow::Result;
use serde::{Deserialize, Serialize};
use tokio::sync::RwLock;
use tracing::{info, warn};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Quote {
    pub asset: String,
    pub currency: String,
    pub bid: f64,
    pub ask: f64,
    pub ts_ms: i64,
}

#[derive(Default)]
pub struct State {
    quotes: HashMap<String, Quote>,
}

impl State {
    pub async fn update(&mut self, q: Quote) {
        self.quotes.insert(format!("{}/{}", q.asset, q.currency), q);
    }
    pub async fn get(&self, asset: &str, currency: &str) -> Option<Quote> {
        self.quotes.get(&format!("{}/{}", asset, currency)).cloned()
    }
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "info".into()),
        )
        .json()
        .init();

    let state = Arc::new(RwLock::new(State::default()));

    // Spawn ingest loops
    let s = state.clone();
    tokio::spawn(async move { ingest_crypto(s.clone()).await });
    let s = state.clone();
    tokio::spawn(async move { ingest_fx(s.clone()).await });
    let s = state.clone();
    tokio::spawn(async move { broadcast(s.clone()).await });

    info!("realtime-pricing service running");
    tokio::time::sleep(Duration::from_secs(u64::MAX)).await;
    Ok(())
}

async fn ingest_crypto(state: Arc<RwLock<State>>) {
    // In production this connects to Coinbase, Kraken, Binance WebSocket feeds.
    info!("crypto ingest stub");
    loop {
        tokio::time::sleep(Duration::from_secs(1)).await;
    }
}

async fn ingest_fx(state: Arc<RwLock<State>>) {
    info!("fx ingest stub");
    loop {
        tokio::time::sleep(Duration::from_secs(5)).await;
    }
}

async fn broadcast(_state: Arc<RwLock<State>>) {
    info!("ws broadcast stub");
    loop {
        tokio::time::sleep(Duration::from_secs(1)).await;
    }
}

#[allow(dead_code)]
fn dummy() { let _ = warn; }
