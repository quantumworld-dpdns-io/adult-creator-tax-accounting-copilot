//! Prometheus metrics.

use prometheus::{IntCounter, IntCounterVec, Registry, Opts, Histogram, HistogramOpts, register_int_counter_with_registry, register_int_counter_vec_with_registry, register_histogram_with_registry};
use once_cell::sync::Lazy;

pub static REGISTRY: Lazy<Registry> = Lazy::new(Registry::new);

pub static TOOL_CALLS: Lazy<IntCounterVec> = Lazy::new(|| {
    register_int_counter_vec_with_registry!(
        "mcp_tool_calls_total", "Tool invocations", &["tool", "status"], REGISTRY
    ).unwrap()
});

pub static TOOL_LATENCY: Lazy<HistogramVec> = Lazy::new(|| {
    // (declared via custom below)
    HistogramVec::new()
});
