//! MCP server entry point.

use anyhow::Result;
use mcp_server_rust::{config::Settings, server::Server};
use tracing::info;

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::try_from_default_env()
            .unwrap_or_else(|_| "info".into()))
        .json()
        .init();

    let settings = Settings::from_env()?;
    info!(?settings, "starting mcp-server-rust");

    let server = Server::new(settings);
    server.run().await
}
