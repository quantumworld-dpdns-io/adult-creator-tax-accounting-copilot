//! Observability: tracing + OTel exporter init.

use tracing_subscriber::{fmt, EnvFilter};

pub fn init() {
    let _ = fmt()
        .with_env_filter(EnvFilter::try_from_default_env().unwrap_or_else(|_| EnvFilter::new("info")))
        .json()
        .try_init();
}
