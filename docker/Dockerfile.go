# Multi-stage Dockerfile for Go services.
FROM golang:1.27-alpine AS builder

WORKDIR /src
COPY services/mcp-server-go/go.mod services/mcp-server-go/go.sum* ./
RUN go mod download
COPY services/mcp-server-go/ ./
RUN CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags='-s -w' -o /out/mcp-server-go ./cmd/mcp-server-go

FROM gcr.io/distroless/static-debian12:nonroot
COPY --from=builder /out/mcp-server-go /mcp-server-go
USER nonroot:nonroot
EXPOSE 8080
ENTRYPOINT ["/mcp-server-go"]
