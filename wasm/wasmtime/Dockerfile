# Wasmtime standalone runtime image
# Usage: wasmtime --dir=.::/data run /components/tax_form_validator.wasm validate /data/form.json
FROM rust:1.78-slim AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
        pkg-config libssl-dev cmake \
    && rm -rf /var/lib/apt/lists/*
RUN cargo install wasmtime-cli --locked --version "20.0.0"

FROM debian:bookworm-slim
COPY --from=builder /usr/local/cargo/bin/wasmtime /usr/local/bin/wasmtime
WORKDIR /components
COPY components/ /components/
ENTRYPOINT ["/usr/local/bin/wasmtime"]
CMD ["run", "--dir=./::/", "/components/tax_form_validator.wasm"]
