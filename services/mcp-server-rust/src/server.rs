//! MCP server implementation.

use crate::config::Settings;
use anyhow::Result;
use axum::{routing::post, Json, Router};
use serde_json::{json, Value};
use tracing::info;

pub struct Server {
    settings: Settings,
}

impl Server {
    pub fn new(settings: Settings) -> Self {
        Self { settings }
    }

    pub async fn run(self) -> Result<()> {
        match self.settings.transport.as_str() {
            "stdio" => self.run_stdio().await,
            "http" | "streamable-http" => self.run_http().await,
            other => anyhow::bail!("unknown transport: {other}"),
        }
    }

    async fn run_stdio(self) -> Result<()> {
        info!("running stdio MCP transport");
        let stdin = tokio::io::stdin();
        let mut reader = tokio::io::BufReader::new(stdin);
        use tokio::io::AsyncBufReadExt;
        let mut line = String::new();
        loop {
            line.clear();
            let n = reader.read_line(&mut line).await?;
            if n == 0 {
                break;
            }
            let req: Value = serde_json::from_str(line.trim())?;
            let resp = crate::tools::dispatch(&req);
            println!("{}", serde_json::to_string(&resp)?);
        }
        Ok(())
    }

    async fn run_http(self) -> Result<()> {
        let app = Router::new().route("/mcp", post(mcp_handler));
        let addr = format!("{}:{}", self.settings.host, self.settings.port);
        info!(%addr, "running HTTP MCP transport");
        let listener = tokio::net::TcpListener::bind(addr).await?;
        axum::serve(listener, app).await?;
        Ok(())
    }
}

async fn mcp_handler(Json(req): Json<Value>) -> Json<Value> {
    Json(crate::tools::dispatch(&req))
}
